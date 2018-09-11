# -*- encoding:utf-8 -*-
import aiml
import os, sys

from QACrawler import baike
from Tools import Html_Tools as QAT
from Tools import TextProcess as T
from Tools.String_Tools import clean_str
from QACrawler import search_summary
from stock import FinancialData

from flask import Flask,request,render_template,redirect


def qa_web():
    app = Flask(__name__)
    # 绑定访问地址127.0.0.1:5000/user
    @app.route("/qa", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            ques_type = request.form['chose']
            question = request.form['question']
            answer = find_ans(question, ques_type)
            message = str(question) + "\n" + str(answer)
            return render_template('login_t.html', message=message)
        return render_template('login_t.html')
    app.run(host='0.0.0.0', port=5002)


def find_ans(question='', ques_type='0'):
    try:
        if ques_type == '1':
            fd = FinancialData()
            code = question
            try:
                name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb + code + '.html')
            except Exception as e:
                name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb1 + code + '.html')
            return(fd.get_result(name,code,table_name_list,table_date_list,url_list))
        elif ques_type == '0':
            input_message = question
            if len(input_message) > 60:
                return (mybot.respond("句子长度过长"))
            elif input_message.strip() == '':
                return (mybot.respond("无"))
        
            message = T.wordSegment(input_message)
            words = T.postag(input_message)
        
        
            if message == 'q':
                exit()
            else:
                response = mybot.respond(message)
        
                if response == "":
                    ans = mybot.respond('不知道~')
                    return ans
                # 百科搜索
                elif response[0] == '#':
                    # 匹配百科
                    if response.__contains__("searchbaike"):
                        #print "searchbaike"
                        #print (response)
                        res = response.split(':')
                        #实体
                        entity = str(res[1]).replace(" ","")
                        #属性
                        attr = str(res[2]).replace(" ","")
                        #print (entity+'<---->'+attr)
        
                        ans = baike.query(entity, attr)
                        # 命中答案
                        if type(ans) == list:
                            return QAT.ptranswer(ans,False)
                        #elif ans.decode('utf-8').__contains__(u'::找不到'):
                        elif '::找不到' in ans:
                            #百度+Bing
                            #print ("网络查询")
                            ans = search_summary.kwquery(input_message)
        
                    # 匹配不到模版，通用查询
                    elif response.__contains__("NoMatchingTemplate"):
                        #print ("网络查询")
                        ans = search_summary.kwquery(input_message)
        
        
                    if len(ans) == 0:
                        return mybot.respond('不知道~')
                    elif len(ans) >1:
                        result = "答案可能是这个："
                        for a in ans:
                            result += clean_str(a)
                            return result
                    else:
                        return clean_str(ans[0])
                # 匹配模版
                else:
                    return clean_str(response)
    except Exception as e:
        return "换个问题试试~"    


if __name__ == '__main__':

    #初始化jb分词器
    T.jieba_initialize()

    mybot_path = './'
    os.chdir(mybot_path)

    mybot = aiml.Kernel()
    mybot.learn(os.path.split(os.path.realpath(__file__))[0]+"/resources/std-startup.xml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")

    # mybot.respond('Load Doc Snake')
    #载入百科属性列表

    qa_web()    

