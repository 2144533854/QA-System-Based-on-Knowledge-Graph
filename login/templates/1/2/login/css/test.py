#!/usr/bin/env python
# encoding: utf-8

#from django.test import TestCase

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
