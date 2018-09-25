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

raw = True

def qa_web():
    app = Flask(__name__)
    # 绑定访问地址127.0.0.1:5000/user
    @app.route("/qa", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            global raw
            raw = True
            ques_type = request.form['chose']
            question = request.form['question']
            answer, str_log = find_ans(question, ques_type)
            if answer[0] == "是":
                answer = question[0, question.find["是"]] + answer
            elif "为什么" in question:
                answer = "因为" + answer    
            message = "问：" + str(question) + "  答：" + str(answer)
            return render_template('login_t.html', message=message, log=str_log)
        return render_template('login_t.html')
    app.run(host='0.0.0.0', port=5002)


def find_ans(question='', ques_type='0'):
    log = '答案来源：'
    try:
        if ques_type == '1':
            fd = FinancialData()
            code = question
            try:
                name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb + code + '.html')
            except Exception as e:
                name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb1 + code + '.html')
            return(fd.get_result(name,code,table_name_list,table_date_list,url_list), log)
        elif ques_type == '0':
            input_message = question
            if len(input_message) > 60:
                return (mybot.respond("句子长度过长"), log)
            elif input_message.strip() == '':
                return (mybot.respond("无"), log)
        
            message = T.wordSegment(input_message)
            words = T.postag(input_message)
        
        
            if message == 'q':
                exit()
            else:
                response = mybot.respond(message)
        
                if response == "":
                    ans = mybot.respond('不知道~')
                    return (ans, log)
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
                        log += '实体：' + entity + ' 属性：' + attr + '\n'
        
                        ans = baike.query(entity, attr)
                        # 命中答案
                        if type(ans) == list:
                            log += '来自百科图谱\n'
                            return (QAT.ptranswer(ans,False), log)
                        #elif ans.decode('utf-8').__contains__(u'::找不到'):
                        elif '::找不到' in ans:
                            #百度+Bing
                            log += '百科图谱查询不到\n'
                            log += '来自百科摘要+Bing摘要\n'
                            ans = search_summary.kwquery(input_message)
        
                    # 匹配不到模版，通用查询
                    elif response.__contains__("NoMatchingTemplate"):
                        log += '匹配不到模板\n来自百科摘要+Bing摘要\n'
                        ans = search_summary.kwquery(input_message)
                      
        
                    if len(ans) == 0:
                        log += '未查询到答案\n'
                        return (mybot.respond('不知道~'), log)
                    elif len(ans) >1:
                        log += '返回多个答案\n'
                        global raw
                        if raw == False and ('什么是' in question or '是什么' in question):
                            result = "相关内容："
                            for a in ans:
                                result += clean_str(a)
                                return (result, log)
                        else:
                            raw = False
                            question = question.replace("是什么", "").replace("什么是", "")
                            ans1, log1 = find_ans("什么是" + question) 
                            ans2, log2 = find_ans(question + "是什么")
                            if "相关内容" not in ans1:
                                return (ans1, log1)
                            else:
                                return (ans2, log2)
                    else:
                        return (clean_str(ans[0]), log)
                # 匹配模版
                else:
                    log += '匹配问句模板\n'
                    return (clean_str(response), log)
    except Exception as e:
        print(e)
        return ("换个问题试试~", log)    


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

