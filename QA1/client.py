import jieba
import jieba.posseg as pseg
import time
import QA1.search_knowledge as search_knowledge

from QA1.search_W2V import search_W2V
from QA1.question_type import questionType

from flask import Flask,request,render_template,redirect

class Client:
    def __init__(self):
        time_start_total = time.time()
        jieba.load_userdict('./QA1/data/dict/user_dict.txt')
        # jieba.load_userdict('./QA1/data/dict/en_dict.txt')
        # jieba.load_userdict('./QA1/data/dict/pre_dict.txt')
        self.sear = search_W2V()
        self.questype = questionType()
        self.db = search_knowledge.stat()


    # 获取实体及相应候选结果
    def get_entity(self, question):
        entity = ""
        answers = [] 
        if len(self.get_pos(question, "")) != 0:
            entity = self.get_pos(question, "")[0]
            entity, answers = search_knowledge.find(entity, self.db)
        return entity, answers


    # 获取词性分析结果（返回除实体之外的词）
    def get_pos(self, question, entity):
        s = pseg.cut(question)
        relations = []
        for item in s:
            token, pos = item.word, item.flag
            if pos in ['n','nr', 'ns', 'nt', 'nz'] and token != entity:
                relations.append(token)
        return relations


    def qa_find_ans(self, question):
        str_log = ''
        str_return = '不知道~'
        qtype = self.questype.get_type(question)
        cand_relations = self.get_entity(question)
        if cand_relations[0] == "":
            str_log += "找不到问句中的实体\n"
            return str_return, str_log
        else:
            str_log += "问句中的实体：" + cand_relations[0] + "\n"
        if len(cand_relations[1]) == 0:
            str_log += "知识库中找不到问句实体\n"
            return str_return, str_log
        tmp_relation_list = self.get_pos(question, cand_relations[0])
        relation_list = self.questype.ques_type_list(tmp_relation_list, qtype)
        len_rel = len(relation_list)
        if len_rel == 0:
            str_log += "找不到问句中的关系\n"
            return str_return, str_log
        str_return, tmp_log = self.sear.find_answer(cand_relations[1], relation_list)
        str_log += tmp_log
        return str_return, str_log



if __name__ == '__main__':
    # 加载扩充实体
    # mid = EntityExtension()
    # mid.load_alias()
    # 加载word2vec
    time_start_total = time.time()
    jieba.load_userdict('./data/dict/user_dict.txt')
    # jieba.load_userdict('./data/dict/en_dict.txt')
    # jieba.load_userdict('./data/dict/pre_dict.txt')
    time_end_loadDict = time.time()
    print("加载用户字典用时:", time_end_loadDict - time_start_total)
    sear = search_W2V()
    time_end_searchW2c = time.time();
    print("加载w2c文件用时:",time_end_searchW2c-time_end_loadDict,"\n")
    questype = questionType()
    time_end_questype = time.time();
    print("加载问题类型模块用时：",time_end_questype-time_end_searchW2c,"\n")
    c = Client()
    c.qa_web()

