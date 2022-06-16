

# from ac自动 import *
# from 查询结果 import *
# from 查询neo4j import *

'''问答类'''
import datetime

from QAsystem.ac自动 import QuestionClassifier
from QAsystem.查询neo4j import QuestionPaser
from QAsystem.查询结果 import AnswerSearcher


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.debug=True

    def change_debug_status(self):
        self.debug=not self.debug# 相当于开关，每次调用都会取反

    def add_cost_time(self,t1,s,s2):
        if self.debug:
            t2 = datetime.datetime.now()
            cost_time= str(t2 - t1).replace('0:00:0','').replace('0:00:','')
            return s2+s+f'\n      耗时{cost_time}秒'
        else:
            return s
    def chat_main(self, sent):
        answer = '抱歉，本系统暂时无法回答您的问题。'
        # 问句分类
        t1 = datetime.datetime.now()
        res_classify = self.classifier.classify(sent)
        print(res_classify)
        if not res_classify:
            return answer
        # 问句解析
        s1="answer_from_redis"
        s2="answer_from_neo4j"

        res_sql,qtype = self.parser.parser_main_redis(res_classify)#先从redis里查询
        answer_from_redis= self.searcher.search_main_redis(res_sql,qtype)
        if answer_from_redis!='未查询到数据':
            return self.add_cost_time(t1,answer_from_redis,s1)
        else:
            res_sql, qtype = self.parser.parser_main(res_classify)#这里开始从neo4j里查询

            final_answers = self.searcher.search_main(res_sql, qtype)
            if not final_answers:
                return self.add_cost_time(t1,answer,None)
            else:
                return self.add_cost_time(t1,final_answers,s2)

# if __name__ == '__main__':
#     handler = ChatBotGraph()
#     while 1:
#         question = input('用户:')
#         answer = handler.chat_main(question)
#         print('小助手:', answer)



















