# -*- coding:utf-8 -*-
import subprocess
import os
class questionType:
        def Person_type(self,list):
            for word in list:
                if word ==u'谁':
                    list.append(u'职业')
            return list

        def Number_type(self,list):
            for word in list:
                if word ==u'生日':
                    list.append(u'出生日期')
                if word ==u'时候':
                    list.append(u'日期')
                    list.append(u'时间')
            return list

        def Location_type(self,list):
            for word in list:
                if word ==u'哪':
                    list.append(u'地理位置')
                    list.append(u'所属地区')
                    list.append(u'地点')
                if word ==u'国人':
                    list.append(u'国籍')
            return list

        def object_type(self,list):
            for word in list:
                if word ==u'干什么':
                    list.append(u'职业')
                    list.append('BaiduTAG')
            return list

        def null_type(self,list):
            for word in list:
                if word ==u'属':
                    list.append(u'生肖')
            return list

        def ques_type_list(self,list,types):
            # file = open('D:/Desktop/Cstopword.txt','r')
            # stop_lists = file.readlines();
            # stop_list =[]
            # for stop_word in stop_lists:
            #     stop_word = stop_word.strip()
            #     stop_list.append(stop_word)
            # for word in list:
            #     if word in stop_list:
            #         list.remove(word)
            stopword = [line.strip() for line in open('./QA1/stopword.txt','r')]
            for word in list:
                if word in stopword:
                    list.remove(word)
            if len(list)>=3:
                return list
            if types=='person':
                list =self.Person_type(list)
                return list
            elif types=='location':
                list =self.Location_type(list)
                return list
            elif types=='object':
                list = self.object_type(list)
            elif types=='null':
                list = self.null_type(list)
            return list

        #import os.path
        # def correct(question):
        #     jarpath = os.path.join(os.path.abspath('.'),'G:/Desktop/')
        #     startJVM(getDefaultJVMPath(),'-ea','-Djava.class.path=%s'%(jarpath+'pattern.jar'))
        #     JDClass = JClass("QA.tiny_QA.tinyQA")
        #     jd = JDClass()
        #     jprint = java.lang.System.out.printIn
        #     jprint(jd.GetPatten(question))
        #     shutdownJVM()
        def get_type(self,question):
            command = subprocess.Popen(['java','-jar','pattern.jar',question],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            quesType = (str(command.stdout.read()))[2:-3]
            return quesType
            # #quesType = (str(command).split('\n'))[-1]
            # command = str(command).strip().split('\n')
            # print (command[-1])
            # #return quesType
            # command = os.popen('java -jar pattern.jar '+question)
            # commands = str(command.read()).strip().split('\n')
            # return (commands[-1])

if __name__ == '__main__':
    question = u'姚明的体重是多少'
    qtype = questionType()
    print(qtype.get_type(question))
