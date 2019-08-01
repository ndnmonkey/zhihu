import requests
import re,urllib
from bs4 import BeautifulSoup
import random
import os, os.path


#在西刺找代理
def getproxies(url):
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]

    try:
        r = requests.get(url, headers=random.choice(headers), timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        content = r.text
    except:
        return "It is failed to get html!"
    else:
        bsObj = BeautifulSoup(content, "html.parser")
        ips = bsObj.find_all('tr')
        # print(ips[1])
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)  #这里一句话就取代了下面的正则
            # ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            # ip_result = re.findall(ip_pattern, str(class_country), flags=0)
            # print(ip_result)
            # port_pattern = re.compile(r'\>\d{4,5}\<')
            # port = re.findall(port_pattern, str(class_country), flags=0)
            # print(port)
            # pattern = re.compile(r'\d{4,5}')
            # port_result = re.findall(pattern, str(port[0]), flags=0)
            # print(port_result)
        # print(ip_list)
        for ip in ip_list:
            try:
                proxy_host = "https://" + ip
                proxy_temp = {"https": proxy_host}
                res = urllib.urlopen(url, proxies=proxy_temp).read()
            except Exception as e:
                ip_list.remove(ip)
                continue
        # print(ip_list)
        # return ip_list

        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        # print(proxies)
        return proxies


def gethtml(url):
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    try:
        r = requests.get(url, headers=random.choice(headers),proxies=getproxies('https://www.xicidaili.com/nn'), timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text

        f = open("1.txt", mode="a+", encoding="utf-8")
        f.write(html)
        f.flush()
        f.close()
        # print(html)
        return html

    except:
        return "It is failed to get html!"

def jiexi(html):
    f = open("1.txt", mode="r+", encoding="utf-8")
    content = f.read()
    # print("第一次运行得到的数据")
    f.close()

    link_list = []
    bsObj = BeautifulSoup(content, "html.parser")
    # print(bsObj)
    results = bsObj.find_all('div', {"class": "vrwrap"})
    dict = {}
    for result in results:
        link_list.append(result.find_all('a')[1]['href'])
        key = result.find_all('a')[0].text
        value =  result.find_all('a')[1]['href']
        if value[0:4] != 'http':
            value = "https://www.sogou.com" + value
        dict[key] = value
    # print(dict)
    return dict

def get_link(keyword,page):
    link = jiexi(gethtml("https://www.sogou.com/web?query=" + keyword + "&page=" + str(page) + "&ie=utf8"))
    os.remove("1.txt")
    return link

