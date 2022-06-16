
from django.test import TestCase

# Create your tests here.
from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
        pass  # 初始化代码，每个用户只执行一次（比如需要实现登录的操作）

    @task
    def test_job(self):  # 测试代码，模拟多用户反复执行
        four_format_path = []
        for file_format in ['docx', 'doc', 'pdf', 'html']:
            four_format_path.append(
                format_path_dc[file_format][random.sample(range(len(format_path_dc[file_format])), 1)[0]])
        file_path = random.sample(four_format_path, 1)[0]
        r = self.client.post('', files={'file': open(file_path, 'rb')})  # 发post请求，传入文件
        rst = json.loads(r.text)  # r.text是post请求接受的返回值（JSON字符串，复原为原来的对象格式）
        if rst.get('basic_info'):
            print(rst['basic_info'].get('name'), file_path)


class MobileUserLocust(HttpLocust):
    task_set = UserBehavior
    host = 'http://0.0.0.0:5000/'  # 待测试的目标页面
    min_wait = 100
    max_wait = 500

import datetime
str1 = '2018-04-23'
str2 = '2017-03-21'
date1=datetime.datetime.strptime(str1[0:10],"%Y-%m-%d")
date2=datetime.datetime.strptime(str2[0:10],"%Y-%m-%d")
num=(date1-date2).days
print(num)


import sys
import os
from glob import glob

# 获取需要转换的路径
def get_user_path(argv_dir):
    if os.path.isdir(argv_dir):
        return argv_dir
    elif os.path.isabs(argv_dir):
        return argv_dir
    else:
        return False
    # 对转换的TS文件进行排序


def get_sorted_ts(user_path):
    ts_list = glob(os.path.join(user_path, '*.ts'))
    # print(ts_list)
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            # print(os.path.splitext(os.path.basename(ts)))
            file, _ = os.path.splitext(os.path.basename(ts))
            boxer.append(int(file))
    boxer.sort()
    # print(boxer)
    return boxer


# 文件合并
def convert_m3u8(boxer, o_file_name):
    # cmd_arg = str(ts0)+"+"+str(ts1)+" "+o_file_name
    tmp = []
    for ts in boxer:
        tmp.append('/Volumes/192.168.117.81/QQBrowser/视频/.b901020496e22432b15a67e429214f19'+ts)
    cmd_str = '+'.join(tmp)

    import ipdb;ipdb.set_trace()
    exec_str = "cp /b " + cmd_str + ' ' + o_file_name
    # print("cp /b "+cmd_str+' '+o_file_name)
    os.system(exec_str)


if __name__ == '__main__':
    user_path="/Volumes/192.168.117.81/QQBrowser/视频"
    # convert_m3u8('2.ts','4.ts',o_file_name)
    # boxer = get_sorted_ts(user_path)
    boxer=['9.ts', '8.ts', '7.ts', '6.ts', '5.ts', '45.ts', '44.ts', '43.ts', '42.ts', '41.ts', '40.ts', '4.ts', '39.ts', '38.ts', '37.ts', '36.ts', '35.ts', '34.ts', '33.ts', '32.ts', '31.ts', '30.ts', '3.ts', '29.ts', '28.ts', '27.ts', '26.ts', '25.ts', '24.ts', '23.ts', '22.ts', '21.ts', '20.ts', '2.ts', '19.ts', '18.ts', '17.ts', '16.ts', '15.ts', '14.ts', '13.ts', '12.ts', '11.ts', '10.ts', '1.ts', '0.ts']
    o_file_name='1.mp4'
    content=os.walk(user_path)

    # import ipdb;ipdb.set_trace()
    convert_m3u8(boxer, o_file_name)
    # print(os.getcwd())
