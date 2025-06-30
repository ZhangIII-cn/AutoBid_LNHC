import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import time
from fake_useragent import UserAgent
from datetime import datetime
import os
import csv

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

def load_excel(CSV_Set,str="中国政府采购网"):
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



def Spider_Work_CCGP(Keyword_Dict=[],Time_type=1,Region_Dict=[]):
    # Time_type = 1 : 三天内                 Region_Dict为空时 表明选取全部地区
    # Time_type = 2 ：一周内
    # Time_type = 3 : 一月内
    # Time_type = 4 : 近三月
    # Keyword_Dict = ['无人机']  # %E6%97%A0%E4%BA%BA%E6%9C%BA
    Region_Dict = ['辽宁', '大连', '山东', '北京']
    Page_number = 1
    CSV_Set = set()
    print("Working!")
    return





