import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import time

Keyword_Dict=['无人机'] #%E6%97%A0%E4%BA%BA%E6%9C%BA
Region_Dict =['辽宁','大连','山东','北京']
Page_number=45

Headers = [{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Referer': 'https://www.google.com/',  # 模拟从搜索引擎跳转
        # 'Connection': 'keep-alive',
        # 'DNT': '1',  # 禁用追踪
    },#Google Chrome Simulation
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    },#Edge Simulation
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    }, #Firefox
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/107.0.5045.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    },
    {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; 360SE)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Host': 'search.ccgp.gov.cn'
    }
]
Headers_index=4
Headers_number=len(Headers)

for Keyword in Keyword_Dict:    # searchtype = 2 : 搜全文 ; timeType = 2(近一周) 3(近一月)
    time.sleep(1)
    #---------------构造基本Soup：--------------
    url_base = 'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=' + Keyword + '&start_time=2025%3A04%3A02&end_time=2025%3A04%3A09&timeType=3&displayZone=&zoneId=&pppStatus=0&agentName='
    try:
        res = requests.get(url_base, headers=Headers[Headers_index])
        res.encoding = 'utf-8'
        # ---------------获取总页码：-----------------------------------------------------------
        Soup_base = BeautifulSoup(res.text, 'lxml')
        Page_Container = Soup_base.find_all(class_="pager")
        print(Page_Container[0])
    except Exception as e:
        Headers_index=(Headers_index+1) % Headers_number
        res = requests.get(url_base, headers=Headers[Headers_index])
        res.encoding = 'utf-8'
        # ---------------获取总页码：-------------------------------------------------------------
        Soup_base = BeautifulSoup(res.text, 'lxml')
        Page_Container = Soup_base.find_all(class_="pager")
        if len(Page_Container)==0:
            print("被认定为爬虫，请更新策略。")
            exit()
        print(Page_Container[0])

    # ---------------获取每页信息：--------------------------------------------------------------------
    for page_index in range(1,Page_number+1):
        time.sleep(1)
        print(page_index)
        url = 'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index='+str(page_index)+'&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=' + Keyword + '&start_time=2025%3A04%3A02&end_time=2025%3A04%3A09&timeType=2&displayZone=&zoneId=&pppStatus=0&agentName='
        try:
            res = requests.get(url, headers=Headers[Headers_index])
            res.encoding = 'utf-8'
            Soup = BeautifulSoup(res.text, 'lxml')
            Script = Soup.find_all(string=re.compile("ohtmlurls"))
            Str_script = str(Script[0])
        except Exception as e:
            Headers_index = (Headers_index + 1) % Headers_number
            res = requests.get(url, headers=Headers[Headers_index])
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
            Project_name=i.find("a").get_text(strip=True)
            Spans=re.sub(r'\s+', '',i.find("span").text).split('|')  # e.g. 2025.05.1416:00:19|采购人：冠县农业农村局|代理机构：北京广普达工程咨询有限公司中标公告|山东|
            Time_Publishment=Spans[0]
            Perchaser=Spans[1].split("：")[1]
            Agency=Spans[2].split("：")[1]
            Province=Spans[3]
            print(Time_Publishment+" "+Perchaser+" "+Agency+" "+Province)
            # print("-----------------------------")

