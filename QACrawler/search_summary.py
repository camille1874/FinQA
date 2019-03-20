# -*- encoding:utf-8 -*-

import time
from urllib.parse import quote

from Tools import Html_Tools as To
from Tools import TextProcess as T
from Tools.String_Tools import clean_str

'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def kwquery(query):
    #分词 去停用词 抽取关键词
    log = '提取关键词:'
    keywords = []
    words = T.postag(query)
    for k in words:
        # 只保留名词
        if k.flag.__contains__("n"):
            keywords.append(k.word)
            log += k.word
    log += '#' * 50 + '\n'
    answer = []
    text = []
    # 找到答案置1
    flag = 0


    # 抓取百度前10条的摘要
    log += '百度前10条的摘要'
    url = 'https://www.baidu.com/s?wd=' + quote(query)
    log += url + '#' * 50 +'\n'
    soup_baidu = To.get_html_baidu(url)
    
    for i in range(1,11):
        if soup_baidu == None:
            break
        results = soup_baidu.find(id=i)

        if results == None:
            log += '百度摘要找不到答案' + '#' * 50 + '\n'
            break
        log += '第' + str(i) + '条摘要:\n' 
        log += clean_str(results.get_text()) + '#' * 50 +'\n'
        #判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
        #if 'mu' in results.attrs and i == 1:
        if 'mu' in results.attrs and results.find(class_='op_exactqa_s_answer') != None:
            r = results.find(class_='op_exactqa_s_answer')
            log += '第一条百度摘要为百度搜索根据知识图谱直接匹配出的内容，优先查找\n'
            log += '百度知识图谱找到答案' + '#' * 50 + '\n'
            answer.append(r.get_text().strip())
            flag = 1
            break

        #古诗词判断
        if 'mu' in results.attrs and i == 1 and results.find(class_="op_exactqa_detail_s_answer") != None:
            r = results.find(class_="op_exactqa_detail_s_answer") 
            log += '百度诗词找到答案' + '#' * 50 + '\n'
            answer.append(r.get_text().strip())
            flag = 1
            break

        #万年历 & 日期
        if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/calendar'):
            r = results.find(class_="op-calendar-content")
            if r != None: 
                log += '百度万年历找到答案' + '#' * 50 + '\n'
                answer.append(r.get_text().strip().replace("\n","").replace(" ",""))
                flag = 1
                break

        if 'tpl' in results.attrs and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
            r = results.attrs['fk'].replace("6018_","")
            if r != None:
                log += '百度万年历新版找到答案' + '#' * 50 + '\n'
                answer.append(r)
                flag = 1
                break


        #计算器
        if 'mu' in results.attrs and i == 1 and results.attrs['mu'].__contains__('http://open.baidu.com/static/calculator/calculator.html'):
            r = results.find(class_="op_new_val_screen_result")
            if r != None:
                log += '计算器找到答案' + '#' * 50 + '\n'
                answer.append(r.get_text().strip())
                flag = 1
                break


        # 百度知道答案
        #if 'mu' in results.attrs and i == 1:
        if 'mu' in results.attrs and results.find(class_='op_best_answer_question_link') != None:
            r = results.find(class_='op_best_answer_question_link')
            url = r['href']
            zhidao_soup = To.get_html_zhidao(url)
            r = zhidao_soup.find(class_='bd answer').find('pre')
            if r == None:
                r = zhidao_soup.find(class_='bd answer').find(class_='line content')
            log += '百度知道best answer找到答案' + '#' * 50 + '\n'
            answer.append(r.get_text())
            flag = 1
            break

        if results.find("h3") != None:
            # 百度知道
            if results.find("h3").find("a").get_text().__contains__(u"百度知道"):
                url = results.find("h3").find("a")['href']
                if url == None:
                    log += '百度知道找不到答案' + '#' * 50 + '\n'
                    continue
                else:
                    log += '百度知道找到答案' + '#' * 50 + '\n'
                    zhidao_soup = To.get_html_zhidao(url)
                    r = zhidao_soup.find(class_='bd answer')
                    if r == None:
                        continue
                    else:
                        r = r.find('pre')
                        if r == None :
                            r = zhidao_soup.find(class_='bd answer').find(class_='line content')
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 百度百科
            if results.find("h3").find("a").get_text().__contains__(u"百度百科"):
                url = results.find("h3").find("a")['href']
                if url == None:
                    log += '百度百科找不到答案' + '#' * 50 + '\n'
                    continue
                else:
                    log += '百度百科找到答案' + '#' * 50 + '\n'
                    baike_soup = To.get_html_baike(url)

                    r = baike_soup.find(class_='lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break
        text.append(clean_str(results.get_text()) + "(" + results.find("a")['href'] + ")")

    if flag == 1:
        return (answer, log)
    log += '百度前十条摘要不包含百度知道、百度百科内容，或相关内容中找不到答案' + '#' * 50 + '\n'

    #获取bing的摘要
    log += '通过Bing查找\n'
    url = 'https://www.bing.com/search?q=' + quote(query)
    log += url + '\n'
    log += '#' * 50
    soup_bing = To.get_html_bing(url)
    # 判断是否在Bing的知识图谱中
    # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    bingbaike = soup_bing.find(class_="bm_box")

    if bingbaike != None:
        if bingbaike.find_all(class_="b_vList")[1] != None:
            if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
                log += 'Bing百科找到答案' + '#' * 50 + '\n'
                flag = 1
                answer.append(bingbaike.get_text())
                return (answer, log)
    else:
        log += 'Bing百科找不到答案' + '#' * 50 + '\n'
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        for bl in bing_list:
            temp =  bl.get_text()
            if temp.__contains__(u" - 必应网典"):
                url = bl.find("h2").find("a")['href']
                if url == None:
                    log += 'Bing网典找不到答案' + '#' * 50 + '\n'
                    continue
                else:
                    log += 'Bing网典找到答案' + '#' * 50 + '\n'
                    bingwd_soup = To.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break

        if flag == 1:
            return (answer, log)



    log += '没有找到答案，返回百度前十条摘要内容\n'
    #if flag == 0:
        #分句
        #log += ''
        #cutlist = ["。", "?", ".", "_", "-", "：", "！", "？"]
        #temp = ''
        #sentences = []
        #for i in range(0,len(text)):
        #    if text[i] in cutlist:
       #         if temp == '':
       #             continue
       #         else:
       #             sentences.append(temp)
       #         temp = ''
       #     else:
       #         temp += text[i]
       #        
       # # 找到含有关键词的句子,去除无关的句子
       # key_sentences = {}
       # for s in sentences:
       #     for k in keywords:
       #         if k in s:
       #             key_sentences[s]=1


        # 根据问题制定规则
        # 识别人名
        #target_list = {}
        #for ks in key_sentences:
        #    # print ks
        #    words = T.postag(ks)
        #    for w in words:
        #        if w.flag == ("nr"):
        #            if w.word in target_list:
        #                target_list[w.word] += 1
        #            else:
        #                target_list[w.word] = 1

        ## 找出最大词频
        #sorted_lists = sorted(target_list.items(), key=lambda x: x[1], reverse=True)
        #去除问句中的关键词
        #sorted_lists2 = []
        # 候选队列
        #for i, st in enumerate(sorted_lists):
        #    if st[0] in keywords:
        #        continue
        #    else:
        #        sorted_lists2.append(st)
        ##log += ' '.join(sorted_lists2)
        ##print ("返回前n个词频")
        #answer = []
        #for i,st in enumerate(sorted_lists2):
        #    if i< 3:
        #        answer.append(st[0])
        #for ks in key_sentences:
        #    answer += ks + '\n'         
    answer = text       

    return (answer,log)

