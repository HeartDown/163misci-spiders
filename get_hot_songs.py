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
import json
import setting
#http://music.163.com/song/media/outer/url?id=ID数字.mp3  网易云音乐的外链歌曲真实地址
artists_value = []
songs_value = []
start_data = 0
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
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/66.0.3359.181 Safari/537.36'}
    proxies = ip_list[random.randint(0,len(ip_list))]
    try:
        time.sleep(3)#设置时间间隔为3秒
        r = requests.get(url, headers=headers,proxies=proxies)
        r.encoding = "utf-8"
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
    items = soup.find('textarea', id='song-list-pre-data')
    return json.loads(items.text)


# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(items, artist_name,artist_id):
    for item in items:
        song_id=item['id']
        print('歌曲id:', song_id)
        song_name = item['name']
        print('歌曲名字:', song_name)
        songs_value.append((song_id,song_name,artist_id))

# 获取歌手id和歌手姓名
def read_csv():
    with open("music163_artists.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            if artist_id=="artist_id":
                continue
            else:
                yield artist_id, artist_name
    # 当程序的控制流程离开with语句块后, 文件将自动关闭

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
    for readcsv in read_csv():
        artist_id, artist_name = readcsv
        artists_value.append((artist_id,artist_name))
        url = "https://music.163.com/artist?id=" + str(artist_id)
        print("正在获取{}的热门歌曲...".format(artist_name))
        html = get_html_src(url)
        items = parse_html_page(html)
        print("{}的热门歌曲获取完成!".format(artist_name))
        print("开始将{}的热门歌曲写入文件".format(artist_name))
        write_to_csv(items, artist_name,artist_id)
        print("{}的热门歌曲写入到本地成功!".format(artist_name))
        if len(artists_value)>1000 and len(artists_value)>1000:
            artist_sql="insert into artist_info(artist_id, artist_name) values(%s, %s) ON DUPLICATE KEY UPDATE artist_id=VALUES(artist_id),artist_name=VALUES(artist_name);"
            song_sql="insert into song_info(song_id, song_name,artist_id) values(%s, %s, %s) ON DUPLICATE KEY UPDATE song_id=VALUES(song_id),song_name=VALUES(song_name),artist_id=VALUES(artist_id);"
            insertDb(artist_sql,artists_value)
            insertDb(song_sql,songs_value)
    

if __name__ == "__main__":
    main()
