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
from QA1.client import Client
raw = True

def qa_web():
    app = Flask(__name__)
    # 绑定访问地址127.0.0.1:5002/qa
    @app.route("/qa", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            global raw
            raw = True
            #ques_type = request.form['chose']
            question = request.form['question']
            #answer, str_log = find_ans(question, ques_type)
            answer, str_log = find_ans(question)
            if answer != "" and answer[0] == "是":
                answer = question[:question.find["是"]] + answer
            elif "为什么" in question:
                answer = "因为" + answer    
            message = "问：" + str(question) + "  答：" + str(answer)
            return render_template('login_t.html', message=message, log=str_log)
        return render_template('login_t.html')
    app.run(host='0.0.0.0', port=5002)


#def find_ans(question='', ques_type='0'):
def find_ans(question=''):
    global raw
    log = '答案来源：'
    cnt = 0
    input_message = question
    if len(input_message) > 60:
        return (mybot.respond("句子长度过长"), log)
    elif input_message.strip() == '':
        return (mybot.respond("无"), log)

    # 检索本地知识库得到答案，代码在QA1文件夹
    cnt += 1
    log += str(cnt) + ':检索本地知识库\n'
    old_client = Client()
    ans, log_tmp = old_client.qa_find_ans(input_message)
    log += log_tmp
    if ans != "不知道~":
        return (clean_str(ans), log)        
    log += '本地知识库找不到答案或答案不确定\n' 


    message = T.wordSegment(input_message)

    response = mybot.respond(message)
    # log += 'AIML模板返回内容:' + response + '\n'
    if response == "":
        ans = mybot.respond('不知道~')
        return (ans, log)
    elif response[0] == '#':
        cnt += 1
        log += str(cnt) + ':匹配不到问句模板\n'
        if response.__contains__("searchbaike"):
            res = response.split(':')
            entity = str(res[1]).replace(" ","")
            attr = str(res[2]).replace(" ","")
            cnt += 1
            log += str(cnt) + ':匹配到实体属性模板,' + '实体:' + entity + ' 属性:' + attr + '\n'
            ans = baike.query(entity, attr)
            if type(ans) == list:
                cnt += 1
                log += str(cnt) + ':来自百科Infobox\n'
                return (QAT.ptranswer(ans,False), log)
            elif '-找不到' in ans:
                cnt += 1
                log += str(cnt) + ':百科Infobox查询不到:' + ans + '\n'
                cnt += 1
                log += str(cnt) + '来自搜索\n'
                (ans, tmplog) = search_summary.kwquery(input_message)
                log += tmplog                    

        elif response.__contains__("NoMatchingTemplate"):
            cnt += 1
            log += str(cnt) + ':匹配不到实体关系模板\n'
            cnt += 1
            log += str(cnt) + ':来自搜索\n'
            (ans,tmplog) = search_summary.kwquery(input_message)
            log += tmplog

        if len(ans) == 0:
            cnt += 1
            log += str(cnt) + ':未查询到答案\n'
            return (mybot.respond('不知道~'), log)

        elif len(ans) >1:
            cnt += 1
            log += str(cnt) + ':返回百度摘要\n'
            if raw == False and ('什么是' in question or '是什么' in question):
                result = "给你找到几篇新闻："
                for a in ans:
                    result += a + '\n'
                return (result, log)
            else:
                raw = False
                question = question.replace("是什么", "").replace("什么是", "")
                ans2, log2 = find_ans(question + "是什么")
                ans1, log1 = find_ans("什么是" + question) 
                if "给你找到几篇新闻" not in ans1:
                    return (ans1, log1)
                else:
                    return (ans2, log2)
        else:
            return (clean_str(ans[0]), log)



    # 直接匹配问句模版
    else:
        cnt += 1
        log += str(cnt) + ':匹配问句模板\n'
        return (clean_str(response), log)
    #except Exception as e:
    #    print(e)
    #    return ("换个问题试试~", log)    


if __name__ == '__main__':
    T.jieba_initialize()

    mybot_path = './'
    os.chdir(mybot_path)

    mybot = aiml.Kernel()
    mybot.learn(os.path.split(os.path.realpath(__file__))[0]+"/resources/std-startup.xml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/xiaohuangji.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/ordinary_question.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/common_conversation.aiml")

    qa_web()    

