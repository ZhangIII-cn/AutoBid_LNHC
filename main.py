import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import time
from fake_useragent import UserAgent
from datetime import datetime
import os
import csv

Keyword_Dict=['无人机'] #%E6%97%A0%E4%BA%BA%E6%9C%BA
Region_Dict =['辽宁','大连','山东','北京']
Page_number=1
CSV_Set=set()

def get_headers():
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn',
        # 'referer':'https://www.ccgp.gov.cn/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'cache-control':'max-age=0',
        'connection': 'keep-alive'
    }
    return headers

def load_excel(str="中国政府采购网"):
    # 检查该行数据是否已存在于表中 --------------------------------------------------------------------
    Filename = str + f"标书信息_{datetime.now().strftime('%Y_%m_%d')}.csv"
    file_exists = os.path.isfile(Filename)
    if not file_exists:
        print("文件不存在")
        return
    with open(Filename, mode="r", newline="", encoding="ansi") as f:
        reader = csv.DictReader(f)
        for row in reader:
            value=row['项目名称']
            CSV_Set.add(value)


def write_excel(Output_list,str="中国政府采购网"):
    Time_Publishment = Output_list['Time_Publishment']
    Perchaser = Output_list['Perchaser']
    Agency = Output_list['Agency']
    Province = Output_list['Province']
    Project_name=Output_list['Project_name']
    Project_type=Output_list['Project_type']
    # print(Time_Publishment + " " + Perchaser + " " + Agency + " " + Province + ":" + Project_name + " " + Project_type)
    Filename = str+f"标书信息_{datetime.now().strftime('%Y_%m_%d')}.csv"
    # 检查文件是否存在----------------------------------------------------------
    file_exists = os.path.isfile(Filename)
    # 写入文件（追加或新建）
    with open(Filename, mode="a" if file_exists else "w", newline="", encoding="ansi") as f:
        writer_dict = csv.DictWriter(f,fieldnames=Output_list.keys())
        writer = csv.writer(f)
        # 如果是新文件，先写入表头
        if not file_exists:
            writer.writerow(['发布日期','采购部门','代理机构','省份','项目名称','公告类型','项目链接'])


        # 写入数据（自动追加到末尾）
        writer_dict.writerow(Output_list)
    # print(f"数据已{'追加' if file_exists else '新建'}至文件: {Filename}")
    return



# ----------------------   MAIN   -------------------------------------------------------------
load_excel()
for Keyword in Keyword_Dict:   # searchtype = 2 : 搜全文 ; timeType = 2(近一周) 3(近一月)
    time.sleep(1)
    #---------------构造基本Soup：--------------
    url_base = 'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=' + Keyword + '&start_time=2025%3A05%3A13&end_time=2025%3A05%3A20&timeType=2&displayZone=&zoneId=&pppStatus=0&agentName='
    try:
        headers=get_headers()
        res = requests.get(url_base, headers=headers)
        res.encoding = 'utf-8'
        # ---------------获取总页码：-----------------------------------------------------------
        Soup_base = BeautifulSoup(res.text, 'lxml')
        Page_Container = Soup_base.find_all(class_="pager")
        tmp=Page_Container[0]
    except Exception as e:
        headers=get_headers()
        res = requests.get(url_base, headers=headers)
        res.encoding = 'utf-8'
        # ---------------获取总页码：-------------------------------------------------------------
        Soup_base = BeautifulSoup(res.text, 'lxml')
        Page_Container = Soup_base.find_all(class_="pager")
        if len(Page_Container)==0:
            print("被认定为爬虫，请更新策略。")
            exit()

    str_right=Page_Container[0].script.string.split("size:", 1)[-1].lstrip()
    Page_number=int(str_right.split(',')[0])

    # ---------------获取每页信息：--------------------------------------------------------------------
    for page_index in range(1,Page_number+1):
        if page_index<8:
            time.sleep(3)
        else :
            time.sleep(5)
        print(page_index)  # searchtype = 2 : 搜全文 ; timeType = 2(近一周) 3(近一月)
        url = 'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index='+str(page_index)+'&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=' + Keyword + '&start_time=2025%3A05%3A13&end_time=2025%3A05%3A20&timeType=2&displayZone=&zoneId=&pppStatus=0&agentName='
        #      https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=2                  &bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw= %E6%97%A0%E4%BA%BA%E6%9C%BA&start_time=2025%3A05%3A12&end_time=2025%3A05%3A19&timeType=2&displayZone=%E5%85%A8%E9%83%A8&zoneId=&pppStatus=0&agentName=
        try:
            headers=get_headers()
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            Soup = BeautifulSoup(res.text, 'lxml')
            Script = Soup.find_all(string=re.compile("ohtmlurls"))
            Str_script = str(Script[0])
        except Exception as e:
            headers=get_headers()
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            Soup = BeautifulSoup(res.text, 'lxml')
            Script = Soup.find_all(string=re.compile("ohtmlurls"))
            if len(Script) == 0:
                print("被认定为爬虫，请更新策略。")
                exit()
            Str_script = str(Script[0])

        # ----------------------获取当前页中所有ul项的url链接-----------------------------------------------
        Str_url = re.findall(r'"([^"]*)"', Str_script)
        URL_list = Str_url[0].split(',')
        # print(URL_list)

        UL_list = Soup.find_all("ul", class_="vT-srch-result-list-bid")
        Li_list=UL_list[0].find_all('li')
        for index in range(len(Li_list)):
            i=Li_list[index]    # i is tag type
            # print(i)
            Project_name=i.find("a").get_text(strip=True)
            Project_type=i.find("strong").get_text(strip=True)
            Spans=re.sub(r'\s+', '',i.find("span").text).split('|')  # e.g. 2025.05.1416:00:19|采购人：冠县农业农村局|代理机构：北京广普达工程咨询有限公司中标公告|山东|
            Time_Publishment=Spans[0]
            Perchaser=Spans[1].split("：")[1]
            Agency=Spans[2].split("：")[1]
            Province=Spans[3]
            Output_list={'Time_Publishment':Time_Publishment,'Perchaser':Perchaser,'Agency':Agency,'Province':Province,'Project_name':Project_name,'Project_type':Project_type,'URL':URL_list[index]}
            if Project_name not in CSV_Set:
                write_excel(Output_list)
            else:
                print("信息已存在")
            # exit()#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # print("-----------------------------")

