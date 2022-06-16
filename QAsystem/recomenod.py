import datetime
import json
import os
import random

'''
为了提高运行速度，这么设计这个数据类
1、首先对于django系统，文件读写一律用绝对路径
2、秉持一次读写，多次复用原则，只从json/text读取一次数据，其余数据子集从父集里面抽取
3、__init__初始化，在将推荐算法计算的同时，将分数加入总数据并保存为成员变量，方便多次复用
4、数据类只负责处理数据，被绘制类调用
'''

type=['其它展会','机械/五金/工业','医疗保健','能源化工','节能环保','电子光电','IT通信','数码家电','休闲旅游','餐饮食品','汽车交通','纺织鞋服','房产建材','文体办公','百货家居','礼品工艺','经贸综合','妇婴玩具','农林渔牧','珠宝首饰','劳保安防','广告传媒']


class DataForChart(object):
    def __init__(self):
        self.all_expo_data, self.a1,self.a4, self.start_time = self.get_recommend_data()
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.temp1 = os.path.join(cur_dir, '词库/展会名称.txt')
        self.temp2 = os.path.join(cur_dir, '词库/展会类型.txt')
        self.temp3 = os.path.join(cur_dir, '词库/展览地点.txt')
        self.temp4 = os.path.join(cur_dir, '词库/所在国家.txt')
        self.temp5 = os.path.join(cur_dir, '词库/月份.txt')
        self.temp6 = os.path.join(cur_dir, '词库/年份.txt')
        self.temp7 = os.path.join(cur_dir, '词库/组织机构2.txt')
        self.name = [i.strip() for i in open(self.temp1, encoding='utf-8') if i.strip()]
        self.type = [i.strip() for i in open(self.temp2, encoding='utf-8') if i.strip()]
        self.place = [i.strip() for i in open(self.temp3, encoding='utf-8') if i.strip()]
        self.country = [i.strip() for i in open(self.temp4, encoding='utf-8') if i.strip()]
        self.month = [i.strip() for i in open(self.temp5, encoding='utf-8') if i.strip()]
        self.year = [i.strip() for i in open(self.temp6, encoding='utf-8') if i.strip()]
        self.orgization = [i.strip() for i in open(self.temp7, encoding='utf-8') if i.strip()]

        self.expo_orgization = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-组织机构2.txt'), encoding='utf-8') if
                                i.strip()]
        self.expo_place = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-展览地点.txt'), encoding='utf-8') if
                           i.strip()]
        self.expo_type = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-展会类型.txt'), encoding='utf-8') if
                          i.strip()]
        self.expo_country = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-所在国家.txt'), encoding='utf-8') if
                             i.strip()]
        self.expo_month = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-月份.txt'), encoding='utf-8') if
                           i.strip()]
        self.expo_year = [i.strip() for i in open(os.path.join(cur_dir, f'词库/展会-年份.txt'), encoding='utf-8') if
                          i.strip()]

    def get_len_and_name(self):
        expo_len = [len(self.orgization), len(self.name), len(self.place), len(self.country), len(self.type),
                    len(self.year), len(self.month)]
        expo_name = ['组织机构', '展会', '展览地点', '国家', '展会类型', '年份', '月份']
        return expo_len, expo_name

    def get_len_and_name2(self):
        expo_len = [len(set(self.expo_orgization)), len(set(self.name)), len(set(self.place)), len(set(self.country)),
                    len(set(self.type)), len(set(self.year)), len(set(self.month))]
        return expo_len, ['组织机构', '展览地点', '展会类型', '举办国家', '举办月份', '举办年份']

    def delnum(self, s):
        for i in range(0, 5):
            if s[i].isdigit() and s:
                s = s[i + 1:]
        if s[0].isdigit() and s:
            s = s[1:]
        return s.replace('年', '')

    def get_recommend_data(self):
        str1 = '2018-04-23'
        str2 = '2017-03-21'
        date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
        date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
        num = (date1 - date2).days

        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        f = open(os.path.join(cur_dir, '词库/data4.json'), 'r')
        f1 = json.load(f)
        dict1 = {}
        all_expo_data = {}
        start_time = []

        for i in range(1, 54617):  # 逐行读取,54617个
            try:
                data_json = f1[str(i)]
                all_expo_data[i] = data_json
                str1 = data_json["开始时间"].replace('_', '-').replace('.', '-').replace('年', '-').replace('月', '-')

                start_time.append(str1)
                # str2=data_json["结束时间"].replace('_','-').replace('.','-')
                pnum = data_json['感兴趣人数']

                num = abs((datetime.datetime.strptime(str(datetime.datetime.now())[0:10],
                                                      "%Y-%m-%d") - datetime.datetime.strptime(str1[0:10],
                                                                                               "%Y-%m-%d")).days)
                data_json['score'] = num
                # print(num,pnum)
                score = int(pnum) / (num + 2) ** 0.5
                dict1[str(i)] = score
            except Exception as e:
                pass
            continue
            # print(score)
        a1 = sorted(dict1.items(), key=lambda x: x[1])  # 抽取出的序号和计算出的分数
        a1.reverse()
        a2 = a1[0:20]
        a3 = []
        a4=[]
        try:
            for i in a2:

                data=all_expo_data[int(i[0])]
                if data['展会类型']=='':
                 data['展会类型']=type[random.randint(0,21)]
                a4.append(data)
                a3.append({i[0]:data})
        except Exception:
            pass
        return all_expo_data, a3,a4, start_time

    def get_r_data(self):
        print(self.a4)
        return self.a4

    def get_chart3_data(self):

        charts_year = []
        charts_month_day = []
        for i in self.start_time:
            try:
                charts_year.append(int(i[0:4]) + float(int(i[5:7]) / 12))
                temp = int(i[5:7]) + float(int(i[8:]) / 12)
                charts_month_day.append(temp)
            except Exception as e:
                print(str(e))
            continue

        return charts_year, charts_month_day

    def get_speed_test_data(self):
       return self.a1

#2015中国汽车工程学会年会暨展览会
#2020印度橡胶展