

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径

        self.name = os.path.join(cur_dir, '词库/展会名称.txt')
        self.t = os.path.join(cur_dir, '词库/展会类型.txt')
        self.p = os.path.join(cur_dir, '词库/展览地点.txt')

        self.c = os.path.join(cur_dir, '词库/所在国家.txt')
        self.m = os.path.join(cur_dir, '词库/月份.txt')
        self.y = os.path.join(cur_dir, '词库/年份.txt')
        self.o = os.path.join(cur_dir, '词库/组织机构.txt')
        # 加载特征
        self.name= [i.strip() for i in open(self.name, encoding='utf-8') if i.strip()]
        print('name ok ')
        self.type= [i.strip() for i in open(self.t, encoding='utf-8') if i.strip()]
        print('type ok ')
        self.place= [i.strip() for i in open(self.p, encoding='utf-8') if i.strip()]
        print('place ok ')
        self.country= [i.strip() for i in open(self.c, encoding='utf-8') if i.strip()]
        print('country ok ')
        self.month= [i.strip() for i in open(self.m, encoding='utf-8') if i.strip()]
        print('month ok ')
        self.year= [i.strip() for i in open(self.y, encoding='utf-8') if i.strip()]
        self.orgization = [i.strip() for i in open(self.o, encoding='utf-8') if i.strip()]

        self.region_words = set(self.type + self.name + self.place + self.country + self.month +self.year)
        print('ac ok ')
        # self.region_words = set(self.type + self.name + self.place + self.country + self.month + self.orgization+self.year)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        print('build ok')
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        print('word dict ok')
        # 问句疑问词
        self.type = ['展会类型','风格','种类','类型','特色']
        self.country=['所在国家','举办国家','国家']
        self.hold_place = ['在哪里举办','举办地点','举办地址',"在哪里开幕","在哪里举行",'地址','所在地点','哪些在']
        self.hold_orgization = ['主办方','组织者','协办方',"主办单位","承办单位","特邀单位","支持单位","批准单位","举办方"]
        self.month = ['月', '月份']
        self.year= ['年','年份']

        self.introduction = ['展会概况', '展会情况', '详细情况', '介绍', '概况', '情况', '详情', '大概', '情景']
        self.range = ['范围', '领域', '包括', '方面', '范畴', '规模', '包含', '边界' , '范畴', '包罗', '蕴含',]
        self.cost = ['费用', '花费', '多少钱', '门票', '费用', '人民币', '参加费用', '消费', '开支', '花钱', '代价']
        self.time = ['开始时间', '结束时间', '开始', '结束', '开始日期', '结束日期', '开幕时间', '闭幕时间', '揭幕', '开着', '开启', '关闭']
        self.care = ['留意事项', '注意事项', '留心事项', '小心', '当心', '防备', '小心', '谨慎', '预防', '重视']
        self.way = ['联系方式', '联系', '电话', '地址', '通讯', '到达', '拜访', '参加', '访问', '去', '交通']
        self.count=['人数','多少人','感兴趣人数','吸引']



        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        expo_dict = self.check_medical(question)

        if not expo_dict:
            if 'diseases_dict' in globals():    # 判断是否是首次提问
                expo_dict = expos_dict
            else:
                return {}
        print("expo_dict : ", expo_dict)
        data['args'] = expo_dict
        #收集问句当中所涉及到的实体类型
        types = []

        for type_ in expo_dict.values():
            types += type_

        question_types = []
        question_info = []

#######六大种类
        if self.check_words(self.hold_place, question):
            question_type = 'hold_place'
            question_types.append(question_type)

        if self.check_words(self.hold_orgization, question):
            question_type = 'hold_orgization'
            question_types.append(question_type)

        if self.check_words(self.type, question) :
            question_type = 'type'
            question_types.append(question_type)

        if self.check_words(self.country, question) :
            question_type = 'country'
            question_types.append(question_type)

        if self.check_words(self.year, question) :
            question_type = 'year'
            question_types.append(question_type)

        if self.check_words(self.month, question) :
            question_type = 'month'
            question_types.append(question_type)
####六个内容

        if self.check_words(self.introduction, question):
            question_type = 'introduction'
            question_info.append(question_type)

        if self.check_words(self.count, question):
            question_type = 'count'
            question_info.append(question_type)

        if self.check_words(self.range, question) :
            question_type = 'range'
            question_info.append(question_type)

        if self.check_words(self.cost, question) :
            question_type = 'cost'
            question_info.append(question_type)


        if self.check_words(self.time, question) :
            question_type = 'time'
            question_info.append(question_type)


        if self.check_words(self.care, question) :
            question_type = 'care'
            question_info.append(question_type)

        if self.check_words(self.way, question) :
            question_type = 'way'
            question_info.append(question_type)
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        data['question_info'] = question_info

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.name:
                wd_dict[wd].append('name')
            if wd in self.type:
                wd_dict[wd].append('type')
            if wd in self.place:
                wd_dict[wd].append('place')
            if wd in self.country:
                wd_dict[wd].append('country')
            # if wd in self.orgization:
            #     wd_dict[wd].append('orgization')
            if wd in self.month:
                wd_dict[wd].append('month')
            if wd in self.year:
                wd_dict[wd].append('year')
        return wd_dict

    '''构造actree'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()         # 初始化trie树
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))     # 向trie树中添加单词

        actree.make_automaton()    # 将trie树转化为Aho-Corasick自动机
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如
            wd = i[1][1]      # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)       # stop_wds取重复的短的词
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}  # 获取词和词所对应的实体类型
        global expos_dict
        if final_dict:
            expos_dict = final_dict
        print("final_dict : ",final_dict)
        if 'expos_dict' in globals():
            # print("diseases_dict : ",diseases_dict)
            pass
        else:
            print("expos_dict does not exist.")
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False



# if __name__ == '__main__':
#     handler = QuestionClassifier()
#     while 1:
#         question = input('input an question:')
#         data = handler.classify(question)
#         print(data)