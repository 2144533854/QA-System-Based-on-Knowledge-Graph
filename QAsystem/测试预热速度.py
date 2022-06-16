# # coding: utf-8
# import datetime
# import redis
# from six import itervalues
#
# from QAsystem.ac自动 import QuestionClassifier
# from QAsystem.recomenod import DataForChart
# from QAsystem.查询neo4j import QuestionPaser
# from QAsystem.查询结果 import AnswerSearcher
# from QAsystem.问答系统 import ChatBotGraph
#
# '''
# Redis 操作哈希表，下面这些方法比较常用：
#
# hset：往哈希表中添加一个键值对值
# hmset：往哈希表中添加多个键值对值
# hget：获取哈希表中单个键的值
# hmget：获取哈希表中多个键的值列表
# hgetall：获取哈希表中种所有的键值对
# hkeys：获取哈希表中所有的键列表
# hvals：获取哈表表中所有的值列表
# hexists：判断哈希表中，某个键是否存在
# hdel：删除哈希表中某一个键值对
# hlen：返回哈希表中键值对个数
# '''
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
# r1 = redis.Redis(connection_pool=pool)
# index=[]
#
# def load_to_redis():
#     numlist=[]
#     for data in DataForChart().get_speed_test_data():
#         num=list(data.keys())[0]
#         numlist.append(num)
#         data_json=data[list(data.keys())[0]]
#         index.append({data_json.get('展会名称'):num})
#         for key,value in data_json.items():
#             if key=='组织机构':
#                 for k,v in value.items():
#                     r1.hset(num, k, v)
#             else:
#                 r1.hset(num,key,value)
#     return numlist
# def get_all_value():
#     numlist = load_to_redis()
#     valuelist=[]
#     alllist=[]
#     for i in numlist:
#         valuelist.append({i:r1.hvals(i)})
#         alllist.append({i:r1.hgetall(i)})
#     return valuelist,alllist
# numlist = load_to_redis()
# valuelist,alllist=get_all_value()
#
# def del_all_redis():
#     numlist=load_to_redis()
#     print(numlist)
#     for i in numlist:
#         print(r1.delete(i))
# # list(c1.values())[0]
#
#
# get_all_value()
#
#
#
#
# class QuestionPaserForTest(QuestionPaser):
#
#     def parser_main(self, res_classify):
#         args = res_classify.get('args')
#         entity_dict = super().build_entitydict(args)
#         question_type = res_classify['question_types']
#         question_info = res_classify['question_info']
#         # import ipdb;ipdb.set_trace()
#         if question_info:
#             return entity_dict.get('name')[0],question_info[0]
#         else:
#             return entity_dict.get('name')[0],question_type[0]
#
# class AnswerSearcherForTest(AnswerSearcher):
#
#     def search_main(self, name,qtype):
#         not_find_answers =str
#         answers=dict
#         for i in range(0,len(valuelist)):
#
#             if not name in list(valuelist[i].values())[0]:
#                 not_find_answers= '未查询到数据'
#                 continue
#             else:
#                 answers=alllist[i].get(list(valuelist[i].keys())[0])
#                 answers['name']=answers['展会名称']
#                 final_answer = super(AnswerSearcherForTest, self).answer_prettify(qtype, answers)
#                 return final_answer
#
#         return not_find_answers
#
# # question='2013英国伦敦国际珠宝展（IJL）开幕时间'
# # # data=QuestionClassifier().classify(question)
# # data1={'args': {'2013英国伦敦国际珠宝展（IJL）': ['name']}, 'question_types': [], 'question_info': ['time']}
# # data2={'args': {'2013英国伦敦国际珠宝展（IJL）': ['name']}, 'question_types': [], 'question_info': ['time']}
#
# # # print(QuestionPaser().parser_main(data))
#
# temp1=QuestionClassifier()
# temp2=QuestionPaserForTest()
# temp3=AnswerSearcherForTest()
# temp4=ChatBotGraph()
# def test1(n):
#     t1 = datetime.datetime.now()
#     print("开始时间：" + str(t1))
#     for i in range(n):
#         question = '2013英国伦敦国际珠宝展（IJL）开幕时间'
#         data = temp1.classify(question)
#         name,type=temp2.parser_main(data)
#         temp3.search_main(name,type)
#     t2 = datetime.datetime.now()
#     print("结束时间：" + str(t2))
#     print("耗时:" + str(t2 - t1))
#
# def test2(n):
#     t1 = datetime.datetime.now()
#     print("开始时间：" + str(t1))
#     for i in range(n):
#         question = '2013英国伦敦国际珠宝展（IJL）开幕时间'
#         temp4.chat_main(question)
#
#     t2 = datetime.datetime.now()
#     print("结束时间：" + str(t2))
#     print("耗时:" + str(t2 - t1))
#
#
#
#
#
