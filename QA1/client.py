import jieba
import jieba.posseg as pseg
import time

#from entity_extension import EntityExtension
#from knowledge_base import knowledge_base

import search_knowledge
from search_W2V import search_W2V
from question_type import questionType

#web
from flask import Flask,request,render_template,redirect

class Client:
    # 进行实体扩展并获取(实体，[实体知识列表])
    def get_knowledge(self, question):
        # 1.长实体情况，直接查询知识库
        answer = search_knowledge.find(question)
        if len(answer[1]) == 0:
            # 2.不做实体扩展，查询知识库(别名表有错，所以先用原词查一遍)
            entity = self.get_pos(question)[0]
            answer = search_knowledge.find(entity)
        return answer

    # 获取词性分析结果（实体，[关系列表]）
    def get_pos(self, question):
        s = pseg.cut(question)
        other = []
        result=''
        for item in s:
            token, pos = item.word, item.flag
            if pos in ['nr', 'ns', 'nt', 'nz']:
                if result == '':
                    result = token
            else:
                other.append(token)
        print("entity:"+result+'\n')
        return (result, other)

    def qa_web(self):
        app = Flask(__name__)
        # 绑定访问地址127.0.0.1:5000/user
        @app.route("/qa", methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                question = request.form['question']
                answer ,str_log = self.qa_find_ans(question)
                message = str(question) + "      " + str(answer)
                return render_template('login.html', message=message,log = str_log)
            return render_template('login.html')
        app.run(host='0.0.0.0', port=5001)

    def qa_find_ans(self,question):
        log_file = open('log_temp', 'w')
        str_log = ''
        try:
            if(question == -1):
                return
            time_start_getQuestType = time.time()
            qtype = questype.get_type(question)
            time_end_getQuestType = time.time()
            print("运行 获取问题类型 用时：",time_end_getQuestType-time_start_getQuestType,"\n")
            log_file.writelines("运行 获取问题类型 用时："+str(time_end_getQuestType-time_start_getQuestType)+"\n")
            #print(c.get_knowledge(question))
            # 实体知识列表
            time_start_searchKnowledge = time.time()
            Alist = c.get_knowledge(question)
            time_end_searchKnowledge = time.time()
            print("运行 数据库查询 用时：",time_end_searchKnowledge-time_start_searchKnowledge,"\n")
            print(Alist)
            log_file.writelines("运行 数据库查询 用时："+str(time_end_searchKnowledge-time_start_searchKnowledge)+"\n")
            strss = ''
            for item in Alist[1]:
                strss += str(item[0]) + ' : ' + str(item[1]) + ' ; '
            log_file.writelines(strss+'\n')
            #list = c.get_knowledge(question)[1]
            list = Alist[1]
            # 关系列表
            time_start_getVerb = time.time()
            requlist = c.get_pos(question)[1]
            requlist = questype.ques_type_list(requlist, qtype)
            strss = ''
            for item in requlist:
                strss += str(item) + ' ; '
            log_file.writelines("requlist start :: " + strss  + "requlist end \n")
            time_end_getVerb = time.time()
            print("运行 获取谓词模块 用时：",time_end_getVerb-time_start_getVerb,"\n")
            log_file.writelines("运行 获取谓词模块 用时：" + str(time_end_getVerb-time_start_getVerb)+"\n")
            str_return = sear.find_answer(list,requlist)
            time_end_findAns = time.time()
            print("运行 关系匹配模块 用时：",time_end_findAns-time_end_getVerb,"\n")
            print(str_return)
            log_file.writelines("运行 关系匹配模块 用时：" + str(time_end_findAns-time_end_getVerb) + "\n")
        except Exception as e:
            print("exception",e,'\n')
            print('不知道~')
            str_return = '不知道~'
            log_file.writelines("exception" +  str(e) + '\n')
        log_file.close()
        log_file = open('log_temp')
        for line in log_file:
            str_log += str(line)
        return str_return,str_log
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

