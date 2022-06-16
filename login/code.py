import json

from py2neo import Graph

class datasearch(object):
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            user="neo4j",
            password="123"
        )

    def search1(self,data):
        entities = data

        query = "MATCH (n:`展会`) where n.name='{0}' RETURN n LIMIT 1".format(entities)
        data1=self.g.run(query)
        if not self.g.run(query).data():
            return '未查询到数据'
        else:
            ress = list(tuple(data1)[0])[0]
        # return ress
        return self.type1(ress)

    def search2(self,data,type):
        query = "MATCH p=()-[r:`{0}`]->(q:`{0}`) where q.name='{1}'  RETURN p,q LIMIT 25".format(type,data)
        data1 = self.g.run(query)
        if not self.g.run(query).data():
            return '未查询到数据'
        else:

            ress = list(tuple(data1))
            return self.type2(ress,type)

    def type1(self,d1):
        t1 = d1
        data = [
            {"source": t1.get('name'), "target": t1.get('位置1'), 'rela': '位置1', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('位置2'), 'rela': '位置2', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('开始时间'), 'rela': '开始时间', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('结束时间'), 'rela': '结束时间', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('展会概况').replace('\n','').replace('\'','').replace('\"',''), 'rela': '展会概况', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('展览范围').replace('\n','').replace('\'','').replace('\"',''), 'rela': '展览范围', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('参展费用').replace('\n','').replace('\'','').replace('\"',''), 'rela': '参展费用', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('注意事项').replace('\n','').replace('\'','').replace('\"',''), 'rela': '注意事项', "type": 'resolved'},
            {"source": t1.get('name'), "target": t1.get('联系方式').replace('\n','').replace('\'','').replace('\"',''), 'rela': '联系方式', "type": 'resolved'}
        ]
        return data
    def type2(self,d1,type):
        name=[]
        data=[]
        pname=d1[0].data().get('p').end_node.get('name')

        for i in d1:
            target=i.data().get('p').start_node.get('name')
            if target is None:
                print('target is None')
            data.append(
                {"source": pname, "target": target, 'rela': type, "type": 'resolved'}
            )
        for i in data:
            print(i)
        return data
        # data=[
        #
        #
        #
        # ]
# print(search(1))