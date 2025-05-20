import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import time
from fake_useragent import UserAgent

Keyword_Dict=['无人机'] #%E6%97%A0%E4%BA%BA%E6%9C%BA
Region_Dict =['辽宁','大连','山东','北京']
Page_number=1

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

for Keyword in Keyword_Dict:    # searchtype = 2 : 搜全文 ; timeType = 2(近一周) 3(近一月)
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
        time.sleep(3)
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
        print(URL_list)

        UL_list = Soup.find_all("ul", class_="vT-srch-result-list-bid")
        Li_list=UL_list[0].find_all('li')
        for index in range(len(Li_list)):
            i=Li_list[index]    # i is tag type
            # print(i)
            Project_name=i.find("a").get_text(strip=True)
            Spans=re.sub(r'\s+', '',i.find("span").text).split('|')  # e.g. 2025.05.1416:00:19|采购人：冠县农业农村局|代理机构：北京广普达工程咨询有限公司中标公告|山东|
            Time_Publishment=Spans[0]
            Perchaser=Spans[1].split("：")[1]
            Agency=Spans[2].split("：")[1]
            Province=Spans[3]
            print(Time_Publishment+" "+Perchaser+" "+Agency+" "+Province)
            # exit()#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # print("-----------------------------")

