#-*- encoding:utf-8 -*-
import sys
import requests
import json
import re
from bs4 import BeautifulSoup

class FinancialData():
    def __init__(self):
        self.server = 'http://quotes.money.163.com/'
        self.cwnb = 'http://quotes.money.163.com/hkstock/cwsj_'
        self.cwnb1 = 'http://quotes.money.163.com/usstock/cwsj_'
        
        self.cwzb_dict = {'EPS':'基本每股收益','EPS_DILUTED':'摊薄每股收益','GROSS_MARGIN':'毛利率',
        'CAPITAL_ADEQUACY':'资本充足率','LOANS_DEPOSITS':'贷款回报率','ROTA':'总资产收益率',
        'ROEQUITY':'净资产收益率','CURRENT_RATIO':'流动比率','QUICK_RATIO':'速动比率',
        'ROLOANS':'存贷比','INVENTORY_TURNOVER':'存货周转率','GENERAL_ADMIN_RATIO':'管理费用比率',
        'TOTAL_ASSET2TURNOVER':'资产周转率','FINCOSTS_GROSSPROFIT':'财务费用比率','TURNOVER_CASH':'销售现金比率','YEAREND_DATE':'报表日期'}
        #总表
        self.table_dict = {'cwzb':self.cwzb_dict}
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    
    def get_informations(self, url):
        req = requests.get(url = url, headers = self.headers)
        req.encoding = 'utf-8'
        html = req.text
        page_bf = BeautifulSoup(html, 'lxml')
        #股票名称，股票代码
        name = page_bf.find_all('span', class_ = 'name')[0].string
        # code = page_bf.find_all('span', class_ = 'code')[0].string
        # code = re.findall('\d+',code)[0]

        #存储各个表名的列表
        table_name_list = []
        table_date_list = []
        each_date_list = []
        url_list = []
        #表名和表时间
        table_name = page_bf.find_all('div', class_ = 'titlebar3')
        for each_table_name in table_name:
                        #表名
            table_name_list.append(each_table_name.span.string)
            #表时间
            for each_table_date in each_table_name.div.find_all('select', id = re.compile('.+1$')):
                url_list.append(re.findall('(\w+)1',each_table_date.get('id'))[0])
                for each_date in each_table_date.find_all('option'):
                    each_date_list.append(each_date.string)
                table_date_list.append(each_date_list)
                each_date_list = []
        return name,table_name_list,table_date_list,url_list

    def get_result(self, name, code, table_name_list,table_date_list, url_list):
        result = '股票名:' + name + '\n'
        for i in range(len(table_name_list)):
            #获取数据地址
            url = self.server + 'hk/service/cwsj_service.php?symbol={}&start={}&end={}&type={}&unit=yuan'.format(code,table_date_list[i][-1],table_date_list[i][0],url_list[i])
            req_table = requests.get(url = url, headers = self.headers)
            table = req_table.json()
            nums = len(table)
            value_dict = {}
            for num in range(nums):
                value_dict['股票名'] = name
                value_dict['股票代码'] = code
                for key, value in table[i].items():
                    try:
                        if key in self.table_dict[url_list[i]]:
                            value_dict[self.table_dict[url_list[i]][key]] = value
                    except Exception as e:
                        continue

                for key, value in value_dict.items():
                    if key not in ['股票名','股票代码','报表日期'] and key not in result:
                        result += key + ':' + value + ' '
                value_dict = {}
        return result


if __name__ == '__main__':
    fd = FinancialData()
    code = input('请输入股票代码:')
    name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb + code + '.html')
    print(fd.get_result(name,code,table_name_list,table_date_list,url_list))
