# -*- coding:utf-8 -*-
# import gensim.models
import synonyms
# from gensim.models import Word2Vec
from similarity import Similarity

class search_W2V:
    def __init__(self): 
        # self.mod = gensim.models.KeyedVectors.load_word2vec_format('/home/wangy/wy/QAsystem/word2vec/vector.bin',binary=True)
        self.simi_tool = Similarity()        

    def find_answer(self, knowledge_list, requestion):
        max_value = 0
        ans = "不知道~"
        find = False
        for ques in requestion :
            if find == True:
                break
            for (reword,answer) in knowledge_list:
                if reword == "BaiduTAG":
                    continue
                try:
                    if ques == reword:
                        ans = answer
                        find = True
                        break
                    tmp = self.simi_tool.get_simi(ques, reword)
                    if tmp < 0.8:
                        tmp = synonyms.compare(ques, reword, seg=True)
                        # tmp = self.mod.similarity(ques, reword)
                    if tmp > max_value:
                        max_value = tmp
                        ans = answer
                except:
                    continue
        return ans




