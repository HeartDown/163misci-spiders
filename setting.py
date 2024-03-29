from bs4 import BeautifulSoup
import requests
import random
 
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append({tds[5].text:tds[1].text + ':' + tds[2].text})
    return ip_list
 
def get_proxies():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    return ip_list

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    print(ip_list)
