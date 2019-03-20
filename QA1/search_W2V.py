# -*- coding:utf-8 -*-
# import gensim.models
import synonyms
# from gensim.models import Word2Vec
from QA1.similarity import Similarity

class search_W2V:
    def __init__(self): 
        # self.mod = gensim.models.KeyedVectors.load_word2vec_format('/home/wangy/wy/QAsystem/word2vec/vector.bin',binary=True)
        self.simi_tool = Similarity()        

    # 匹配关系以寻找答案
    def find_answer(self, knowledge_list, ques_relations):
        max_value = 0
        q_rel = "找不到"
        k_rel = "找不到"
        ans = "不知道~"
        log = ""
        find = False
        for ques_relation in ques_relations:
            if find == True:
                break
            for (cand_relation, answer) in knowledge_list:
                if cand_relation == "BaiduTAG" or cand_relation == "BaiduCARD":
                    continue
                try:
                    if ques_relation == cand_relation:
                        ans = answer
                        q_rel = ques_relation
                        k_rel = cand_relation
                        find = True
                        break
                    tmp = self.simi_tool.get_simi(ques_relation, cand_relation)
                    if tmp < 0.8:
                        tmp = synonyms.compare(ques_relation, cand_relation, seg=True)
                        # tmp = self.mod.similarity(ques_relation, cand_relation)
                    if tmp > max_value:
                        max_value = tmp
                        q_rel = ques_relation
                        k_rel = cand_relation
                        ans = answer
                except:
                    continue

        if max_value < 0.8:
            ans = "不知道~"
        log += "问句关系:" + q_rel + "\n"
        log += "匹配到知识库关系：" + k_rel + "(" + str(max_value) + ")\n"
        return ans, log




