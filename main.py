import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

Keyword_Dict=['无人机'] #%E6%97%A0%E4%BA%BA%E6%9C%BA
Region_Dict =['辽宁','大连','山东','北京']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Referer': 'https://www.google.com/',  # 模拟从搜索引擎跳转
    # 'Connection': 'keep-alive',
    # 'DNT': '1',  # 禁用追踪
}

for Keyword in Keyword_Dict:    # searchtype = 2 : 搜全文 ; timeType = 2 :近一周
    url = 'https://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=' + Keyword + '&start_time=2025%3A04%3A02&end_time=2025%3A04%3A09&timeType=2&displayZone=&zoneId=&pppStatus=0&agentName='
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # < div class ="vT_z" style="position:relative" >
    #     < div class ="vT-srch-result" >
    #         < div class ="vT-srch-result-list-con2" >
    #             < div class ="vT-srch-result-list" >
    #                 < ul class ="vT-srch-result-list-bid" >
    Soup=BeautifulSoup(res.text,'lxml')
    UL_list=Soup.find_all("ul",class_="vT-srch-result-list-bid")


    Script=Soup.find_all(string=re.compile("ohtmlurls"))
    Str_script=str(Script[0])
    Str_url=re.findall(r'"([^"]*)"', Str_script)
    URL_list=Str_url[0].split(',')
    print(URL_list)
    Page_Container=Soup.find_all(class_="pager")
    print(Page_Container[0])

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


