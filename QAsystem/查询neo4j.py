
class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify.get('args')
        entity_dict = self.build_entitydict(args)
        question_type = res_classify['question_types']
        question_info = res_classify['question_info']
        import ipdb;ipdb.set_trace()
        if  question_info :
            sql,qtype = self.sql_transfer(question_info[0], entity_dict.get('name')[0])
        else:
            sql,qtype = self.sql_transfer2(question_type, entity_dict)
        return sql,qtype


    def parser_main_redis(self, res_classify):#先从redis里读取
        args = res_classify.get('args')
        entity_dict = self.build_entitydict(args)
        question_type = res_classify['question_types']
        question_info = res_classify['question_info']
        # import ipdb;ipdb.set_trace()
        if question_info:
            return entity_dict.get('name')[0],question_info[0]
        else:
            return None,None


    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        # 查询语句
        query = str

        # import ipdb;
        # ipdb.set_trace()
        if question_type=='time':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='introduction':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='range':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='cost':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='care':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='way':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type
        if question_type=='time':
            query="MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
            return query,question_type

    def sql_transfer2(self, question_type, entities):
        if question_type:
            question_type=question_type[0]
        map={
            'month':'月份',
            'year':'年份',
            'hold_place':'展览地点',
            'place':'展览地点',
            'orgization':'组织机构',
            'country':'所在国家',
            'type':'展会类型',
            'name':'name'
        }
        if not entities:
            return []
        entity=list(entities.items())
        if len(entity)==2:#构造形式如  上海市五月展会有哪些？  的sql  实体+实体
            query="MATCH (r:`{0}`)<-[b:`{0}`]-(x:`展会`)-[p:`{1}`]->(q:`{1}`) where r.name='{2}' and q.name='{3}' RETURN x LIMIT 25"\
                .format(map[entity[0][0]],map[entity[1][0]],entity[0][1][0],entity[1][1][0])
            return query,[map[entity[0][0]],map[entity[1][0]]]
        elif len(entity)==1:
            import ipdb;
            ipdb.set_trace()
            if question_type:#构造形式如  2020菲律宾海事展所在国家  的sql  展会+实体
                query = "MATCH (q)-[r:`{0}`]->(p:`{0}`) where q.name='{1}'  RETURN p LIMIT 25".format(map[question_type] ,entity[0][1][0])
                return query, [map[entity[0][0]]]

            else:#构造形式如  上海的展会有哪些？  的sql  单个实体
                query = "MATCH (p)-[r:`{0}`]->(q:`{0}`) where q.name='{1}'  RETURN p LIMIT 25".format(map[entity[0][0]], entity[0][1][0])
                return query,[map[entity[0][0]]]



'''
hold_place
hold_orgization
type
year
month


'''






# if __name__ == '__main__':
#
#     from ac自动 import QuestionClassifier
#
#     handler = QuestionPaser()
#     QChandler = QuestionClassifier()
#     while 1:
#         question = input('input an question:')
#         data = QChandler.classify(question)
#         print(data)
#         sqls = handler.parser_main(data)
#         print(sqls)