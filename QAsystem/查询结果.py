#!/usr/bin/env python3

import redis
from py2neo import Graph

from QAsystem.recomenod import DataForChart

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r1 = redis.Redis(connection_pool=pool)
index=[]

def load_to_redis():
    numlist=[]
    for data in DataForChart().get_speed_test_data():
        num=list(data.keys())[0]
        numlist.append(num)
        data_json=data[list(data.keys())[0]]
        index.append({data_json.get('展会名称'):num})
        for key,value in data_json.items():
            if key=='组织机构':
                for k,v in value.items():
                    r1.hset(num, k, v)
            else:
                r1.hset(num,key,value)
    return numlist
numlist = load_to_redis()
def del_all_redis():
    numlist=load_to_redis()
    print(numlist)
    for i in numlist:
        print(r1.delete(i))
def get_all_value():
    valuelist=[]
    alllist=[]
    for i in numlist:
        valuelist.append({i:r1.hvals(i)})
        alllist.append({i:r1.hgetall(i)})
    return valuelist,alllist
valuelist,alllist=get_all_value()


# list(c1.values())[0]
class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            user="neo4j",
            password="123"
        )
        self.num_limit = 30

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sql,qtype):
        final_answers = []
        answers = []
        # import ipdb;ipdb.set_trace()
        if not self.g.run(sql).data():
            return '未查询到数据'
        else:
            import ipdb;ipdb.set_trace()
            ress = self.g.run(sql).data()
            final_answer = self.answer_prettify(qtype,ress)
            return final_answer


    def search_main_redis(self, name,qtype):
        not_find_answers =str
        answers=dict
        for i in range(0,len(valuelist)):

            if not name in list(valuelist[i].values())[0]:
                not_find_answers= '未查询到数据'
                continue
            else:
                answers=alllist[i].get(list(valuelist[i].keys())[0])
                answers['name']=answers['展会名称']
                final_answer = self.answer_prettify(qtype, answers)
                return final_answer

        return not_find_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answer):
        final_answer = []
        answers=answer[0]
        if not answers:
            return ''

        if question_type == 'time':
            final_answer = '{0}的开始时间为：{1} ，结束时间为：{2}'.format( answers['n'].get('name'), answers['n'].get('开始时间'), answers['n'].get('结束时间'))

        if question_type == 'introduction':
            final_answer = '{0}的展会概况为：{1} '.format( answers['n'].get('name'), answers['n'].get('展会概况'))

        if question_type == 'range':
            final_answer = '{0}的展览范围为：{1} '.format( answers['n'].get('name'), answers['n'].get('展览范围'))

        if question_type == 'cost':
            final_answer = '{0}的参展费用为：{1} '.format( answers['n'].get('name'), answers['n'].get('参展费用'))

        if question_type == 'care':
            final_answer = '{0}的注意事项为：{1} '.format( answers['n'].get('name'), answers['n'].get('注意事项'))

        if question_type == 'way':
            final_answer = '{0}的联系方式：{1} '.format( answers['n'].get('name'), answers['n'].get('联系方式'))

        if question_type == 'count':
            final_answer = '{0}感兴趣人数：{1} '.format( answers['n'].get('name'), answers['n'].get('感兴趣人数'))



        if type(question_type) is list  :
            # import ipdb;ipdb.set_trace()
            if len(question_type)==1:
                final_answer=f'查询结果为：'
                for i in range(0,len(answer)):
                    final_answer = final_answer+answer[i]['p'].get('name')+'、'
                return final_answer
            elif len(question_type)==2:
                final_answer=f'查询结果为：'
                for i in range(0, len(answer)):
                    final_answer = final_answer + answer[i]['x'].get('name') + '、'
                return final_answer
        return final_answer


# if __name__ == '__main__':
#     searcher = AnswerSearcher()