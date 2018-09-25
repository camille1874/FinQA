# -*- encoding:utf-8 -*-

from Tools import Html_Tools as To
from Tools import TextProcess as T
import os


def get_info(basicInfo_block):
    info = {}
    for bI_LR in basicInfo_block.contents[1:3]:
        for bI in bI_LR:
            if bI.name == None:
                continue
            if bI.name == 'dt':
                tempName = ''
                for bi in bI.contents:
                    tempName += bi.string.strip().replace(u" ",u"")
            elif bI.name == 'dd':
                info[tempName] = bI.contents
    return info

def ptr_Info(info):
    for i in info:
        attr_name = i.encode('utf8').replace(" ","")
        attr_value = str(info[i])
        print ('属性名=  ' + attr_name)
        print ('属性值=  ' + attr_value)


'''
根据实体和属性查询百科列表中的属性值
'''
def query(entity,attr):
    soup = To.get_html_baidu("http://baike.baidu.com/item/"+entity)
    basicInfo_block = soup.find(class_= 'basic-info cmn-clearfix')
    if basicInfo_block == None:
        return attr + "::找不到"
    else:
        info  = get_info(basicInfo_block)
        if attr in info:
            return info[attr]
        else:
            # 同义词判断
            attr_list = T.load_baikeattr_name(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/Attribute_name.txt')
            attr = T.load_synonyms_word_inattr(attr,os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/SynonDic.txt',attr_list)
            if attr in info:
                return info[attr]
            else:
                return attr + "::找不到"

