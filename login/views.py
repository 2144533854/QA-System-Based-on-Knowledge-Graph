import datetime
import hashlib
import json
import os
import sys
import base64
import time

import captcha
import redis
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import jinja2
from django.template import loader

from QAsystem.recomenod import DataForChart
from . import forms
from . import models

# Create your views here.
from .code import  datasearch
from QAsystem.统计可视化 import ChartForExpo
from QAsystem.问答系统 import ChatBotGraph

handler = ChatBotGraph()
def render2(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(**kwargs)

def hash_code(s, salt='login_register'):

    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    pass
    return render(request, 'login/index.html')



def index2(request):
    if request.POST:

        dataa = 1
        data_list = ['展会', '展会类型', '展览地点', '年份', '月份', '组织机构', '所在国家']
        role_name = '名称'

        info = request.POST['q']
        type1=request.POST.get('name')

        search=datasearch()
        data=[]
        if type1=='展会':# 查询展会节点
            data = search.search1(info)
        else:#查询关系节点
            data = search.search2(info,type1)

        if type(data)==str and data=='未查询到数据':
            return render(request, 'login/index2.html',{"data": data, "data_list": data_list, "role_name": role_name})
        context={}

        context['data']=json.dumps(data)
        print(context)
        return render(request,'login/index2.html',{'data':context['data'],"data1": data, "data_list": data_list, "role_name": role_name})


    if request.method=='GET':
        data=1
        data_list=['展会','展会类型','展览地点','年份','月份','组织机构','所在国家']
        role_name='名称'
        return render(request, 'login/index2.html', {"data": data, "data_list": data_list, "role_name": role_name})


def main(request):

    data=DataForChart().get_r_data()
    return render(request, 'login/main.html',{"data": data})


def show(request):
    pass
    return render(request, 'login/main.html')


# def login(request):
#     if request.session.get('is_login', None):
#         return redirect("/index/")


def question(request):
    return render(request, 'login/question.html')


# Create your views here.

# post方式处理问题
def POST(request):

    # handler = ChatBotGraph()
    # 2020年第29届泰国国际塑料及橡胶机械展览会开幕时间

    # handler = ChatBotGraph()
    # question = request.POST.get('question')
    # answer = handler.chat_main(question)
    try :
        answer = handler.chat_main(question)
    except Exception as e:
        print(str(e))
        return  HttpResponse('抱歉，本系统暂时无法回答您的问题')
    return HttpResponse(answer)

def chart(request):
    temp=ChartForExpo()
    chart1=temp.show1()
    chart2=temp.show2()
    chart3=temp.show3()
    args = {"chart1": chart1,"chart2":chart2,"chart3":chart3}

    return render(request,'login/chart.html',args)



pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r1 = redis.Redis(connection_pool=pool)
def login(request):
    if request.session.get('is_login', None):
        return redirect('/question/')  # 跳转页面

    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        username = request.POST.get('username')
        user_info = 'login_user_info' + username
        user_captcha = username + 'user_captcha'
        password = request.POST.get('password')
        captcha = request.POST.get('captcha_1')[0]


        if not r1.exists(user_info):  # user_info也不存在才说明是新用户，否则便是验证码过期的情况
            r1.set(user_captcha, captcha)  # 初始化验证码并设置有效期60
            r1.expire(user_captcha, 60)
            r1.hmset(user_info, {'send': 0, 'login_status': '0', 'fail_time': 0})  # 初始化数据
        elif not r1.exists(user_captcha) and r1.exists(user_info):
            r1.set(user_captcha, captcha)  # 初始化验证码并设置有效期60
            r1.expire(user_captcha, 60)
            return render(request, 'login/login.html', {'message': '验证码已经过期', 'login_form': login_form})

        r1.hincrby(user_info, 'send', amount=1)   # 自增1

        if int(r1.ttl(user_info)) > 1:
            return render(request, 'login/login.html',
                          {'message': f'当前禁止登陆，请等待{time.strftime("%H时:%M分:%S秒", time.gmtime(int(r1.ttl(username))))}',
                           'login_form': login_form})
        print(r1.hgetall(user_info))
        print(r1.hgetall(username))
        if login_form.is_valid():
            if not r1.exists(username):
                print(r1.hgetall(username))
                return render(request, 'login/login.html',
                              {'message': '用户尚未注册', 'login_form': login_form})

            elif int(r1.hget(user_info, 'fail_time')) >= 5:  # 大于5次禁止登陆
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                duration = int(time.mktime(tomorrow.timetuple())) - int(time.time())
                r1.expire(user_info, duration)
                return render(request, 'login/login.html',
                              {'message': '今日错误次数已达五次，请明日再试', 'login_form': login_form})
            elif int(r1.hget(user_info, 'send')) >= 5:
                r1.expire(user_info, 600)
                return render(request, 'login/login.html',
                              {'message': '10分钟内最多请求5次验证码', 'login_form': login_form})
            elif hash_code(password) ==  r1.hget(username, 'password'):
                r1.hset(user_info, 'login_status', 1)
                request.session['is_login']=True
                request.session['user_name']=username
                return redirect('/question/')#跳转页面
            else:
                return render(request, 'login/login.html',
                              {'message': '密码错误', 'login_form': login_form})
        else:
            message = '验证码错误'
            r1.hincrby(user_info, 'fail_time', amount=1)  # 自增1
            if int(r1.hget(user_info, 'fail_time')) >= 5:  # 大于5次禁止登陆
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                duration = int(time.mktime(tomorrow.timetuple())) - int(time.time())
                r1.expire(user_info, duration)
                return render(request, 'login/login.html',
                              {'message': '今日错误次数已达五次，请明日再试', 'login_form': login_form})
            return render(request, 'login/login.html', {'message': message, 'login_form': login_form})
    elif request.method == 'GET':
        login_form = forms.UserForm()
        return render(request, 'login/login.html', locals())



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_info='register_user_info'+username
        user_captcha=username+'user_captcha'
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        captcha = request.POST.get('captcha_1')[0]
        register_form = forms.RegisterForm(request.POST)
        if not r1.exists(user_captcha):
            if not r1.exists(user_info):#user_info也不存在才说明是新用户，否则便是验证码过期的情况
                r1.set(user_captcha, captcha)  # 初始化验证码并设置有效期60
                r1.expire(user_captcha,60)
                r1.hmset(user_info, {'send': 1, 'register_status': '0', 'fail_time': 0})  # 初始化数据
            else:
                r1.set(user_captcha, captcha)  # 初始化验证码并设置有效期60
                r1.expire(user_captcha, 60)
                return render(request, 'login/register.html', {'message': '验证码已经过期', 'register_form': register_form})

        else:
            r1.hincrby(user_info, 'send', amount=1)  # 自增1

        
        if int(r1.ttl(user_info)) > 1:
            return render(request, 'login/register.html',
                          {'message': f'当前禁止注册，请等待{time.strftime("%H时:%M分:%S秒", time.gmtime(int(r1.ttl(user_info))))}',
                           'register_form': register_form})

        if register_form.is_valid() :
            if int(r1.hget(user_info, 'fail_time'))>=5:#大于5次禁止登陆
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                duration = int(time.mktime(tomorrow.timetuple())) - int(time.time())
                r1.expire(user_info,duration)
                return render(request, 'login/register.html', {'message': '今日错误次数已达五次，请明日再试', 'register_form': register_form})
            elif int(r1.hget(user_info, 'send'))>=5:
                r1.expire(user_info, 600)
                return render(request, 'login/register.html', {'message': '10分钟内最多请求5次验证码', 'register_form': register_form})
            elif password1 != password2:
                return render(request, 'login/register.html', {'message': '两次输入的密码不一致', 'register_form': register_form})
            else:
                if r1.hget(user_info,'register_status')=='1':
                    return render(request, 'login/register.html', {'message': "已注册", 'register_form': register_form})
                else:
                    r1.hmset(username, {'password':hash_code(password1)})#
            r1.hset(user_info, 'register_status','1')#此处经过重重检查，能够登陆
            return redirect('/login/')
        else:
            message='验证码错误'
            r1.hincrby(user_info, 'fail_time', amount=1)  # 自增1
            if int(r1.hget(user_info, 'fail_time')) >= 5:  # 大于5次禁止登陆
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                duration = int(time.mktime(tomorrow.timetuple())) - int(time.time())
                r1.expire(user_info, duration)
                return render(request, 'login/register.html',
                              {'message': '今日错误次数已达五次，请明日再试', 'register_form': register_form})
            return render(request, 'login/register.html', {'message': message, 'register_form': register_form})

    elif   request.method == 'GET':
        register_form = forms.RegisterForm()
        return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")
