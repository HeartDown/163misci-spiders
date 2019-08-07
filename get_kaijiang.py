#! /usr/bin/env python
# coding=utf-8
'''

Author: zhouzying
Date: 2018-9-9

'''

import requests
import random
from bs4 import BeautifulSoup
import time
import csv
import pymysql
import re
import json
import setting

keys=["3qihao","3shijian","3jieguo","pailie5","xiaoliang","danxuanzhushu","danxuanjine","zusanzhushu","zusanjine","zuliuzhushu","zuliujine","公告"]
# keys=["排列三开奖期号","排列三开奖时间","排列三开奖结果","排列五","本期销量","单选注数","单选金额","组三注数","组三金额","组六注数","组六金额","公告"]
data_value = []

start_data=0
ip_list = setting.get_proxies()
def get_html_src(url):
    headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Cookie': 'WM_TID=36fj4OhQ7NdU9DhsEbdKFbVmy9tNk1KM; _iuqxldmzr_=32; _ntes_nnid=26fc3120577a92f179a3743269d8d0d9,1536048184013; _ntes_nuid=26fc3120577a92f179a3743269d8d0d9; __utmc=94650624; __utmz=94650624.1536199016.26.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WM_NI=2Uy%2FbtqzhAuF6WR544z5u96yPa%2BfNHlrtTBCGhkg7oAHeZje7SJiXAoA5YNCbyP6gcJ5NYTs5IAJHQBjiFt561sfsS5Xg%2BvZx1OW9mPzJ49pU7Voono9gXq9H0RpP5HTclE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5cb8085b2ab83ee7b87ac8c87cb60f78da2dac5439b9ca4b1d621f3e900b4b82af0fea7c3b92af28bb7d0e180b3a6a8a2f84ef6899ed6b740baebbbdab57394bfe587cd44b0aebcb5c14985b8a588b6658398abbbe96ff58d868adb4bad9ffbbacd49a2a7a0d7e6698aeb82bad779f7978fabcb5b82b6a7a7f73ff6efbd87f259f788a9ccf552bcef81b8bc6794a686d5bc7c97e99a90ee66ade7a9b9f4338cf09e91d33f8c8cad8dc837e2a3; JSESSIONID-WYYY=G%5CSvabx1X1F0JTg8HK5Z%2BIATVQdgwh77oo%2BDOXuG2CpwvoKPnNTKOGH91AkCHVdm0t6XKQEEnAFP%2BQ35cF49Y%2BAviwQKVN04%2B6ZbeKc2tNOeeC5vfTZ4Cme%2BwZVk7zGkwHJbfjgp1J9Y30o1fMKHOE5rxyhwQw%2B%5CDH6Md%5CpJZAAh2xkZ%3A1536204296617; __utma=94650624.1052021654.1536048185.1536199016.1536203113.27; __utmb=94650624.12.10.1536203113',
             'Host': 'music.163.com',
             'Referer': 'http://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'Connection':'close',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/66.0.3359.181 Safari/537.36'}
    proxies = ip_list[random.randint(0,len(ip_list))]
    try:
        requests.session().keep_alive = False
        r = requests.get(url,headers, verify=False)
        # r.encoding = "utf-8"
        if r.status_code == 200:
            # 返回json格式的数据
            return r
    except:
        print("爬取失败!proxies:"+proxies)


def parse_html_page(html):
    # 使用双引号会出现 Unresolve reference
    # pattern = '<span class="txt"><a href="/song?id=(\d*)"><b title="(.*?)">'
    # 这里是使用lxml解析器进行解析,lxml速度快,文档容错能力强,也能使用html5lib
    soup = BeautifulSoup(html.text, 'lxml')
    items = soup.find('tbody', id='kjnum').findAll("tr")
    start_data = re.sub("\D", "",soup.find('span', id='pagenum').text)
    return items
    



def insertDb(sql,value):
    # 打开数据库连接
    config = {
          'host':'39.108.183.195',
          'port':3306,
          'user':'root',
          'password':'hengsha1234',
          'db':'music_server',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
    }
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    cursor.executemany(sql,value)
    db.commit()

def main():
    url = "https://p3.cjcp.com.cn/kaijiang/"
    print("正在获取{}的热门歌曲...")
    parse_html_page(get_html_src(url))

    for index in range(1,start_data):
        url = "https://www.cjcp.com.cn/ajax_kj.php?jsoncallback=&pls_type=page&pagenum="+str(index)
        html = get_html_src(url)
        items = BeautifulSoup(html.text, 'lxml').findAll("tr")
        for index2 in range(len(items)):
            sb={}
            for index3 in range(len(keys)):
                itenindex = index2*len(keys)+index3
                item = re.sub("\D", "",items[0].findAll("td")[itenindex].text.encode('utf-8').decode('unicode_escape'))
                key = keys[index3]
                sb[key]=item
            sb['3jieguo']=sb['pailie5'][0:3]
            data_value.append(sb)
    print("获取成功，正在操作入库..")
    print(data_value)
    print("入库成功..")
    
if __name__ == "__main__":
    main()
