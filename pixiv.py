import urllib.request
import requests
import os
import base64
import hashlib
import re
import time


base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
target_url = 'https://www.pixiv.net/ranking.php?mode=daily'
main_url = 'http://www.pixiv.net'
header = {
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
pixiv_id = 'dubowei123456@qq.com'
password = '730127ly'

def url_open(url):
    req = urllib.request.Request(url)
    respose = urllib.request.urlopen(req)
    html = respose.read()
    return html

def login():
    html = requests.session().get(base_url, headers = header).text
    a = html.find(r'name="post_key" value="')+23
    b = html.find(r'"><',a)
    post_key = html[a:b]
    data = {
        'pixiv_id' : pixiv_id,
        'password' : password,
        'return_to' : main_url,
        'post_key' : post_key
    }
    requests.session().post(login_url,data = data,headers = header)

def get_img(url):
    print(url)
    html = requests.get(url, headers = header).text
    urllist = re.findall(r"data-src=\"(https://i.pximg.net/c/240x480/.+?\.jpg)\"",html)
    for each in urllist:
        if(len(each)>140):
            continue
        print(each)
        print_img(each)
        time.sleep(2)
    urllist = re.findall(r"data-src=\"(https://i.pximg.net/c/240x480/.+?\.png)\"",html)
    for each in urllist:
        if(len(each)>140):
            continue
        print_png(each)
        time.sleep(2)
    
def print_img(urlt):
    url = urlt[:]
    url = url.replace('c/240x480/','')
#    url = url.replace('img-original','c/240x480/img-master')  
#    url = url.replace('','_master1200')
    print(url)
    filename = url.split('/')[-1]
    f = open(filename,'wb')
    req = urllib.request.Request(url)
    req.add_header('referer','https://www.pixiv.net/member_illust.php?mode=medium&illust_id=66952181')
    respose = urllib.request.urlopen(req)
    img = respose.read()
    f.write(img)

def print_png(url):
    url = url.replace('c/240x480/','')
#    url=url.replace('c/240x480/img-master','img-original')  
#    url=url.replace('_master1200','')
    print(url)
    filename = url.split('/')[-1]
    f = open(filename,'wb')
    req = urllib.request.Request(url)
    req.add_header('referer','http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id='+filename.split('_')[0]+'&page=0')
    respose = urllib.request.urlopen(req)
    img = respose.read()
    f.write(img)

def get_num(url):
    html = requests.session().get(url, headers = header).text
    a = html.find('data-id=')+9
    b = html.find(r'">',a)
    return int(html[a:b])
        
def main(folder = 'pixiv',pages = 100):
    month = int(input('请输入你想查找的月份'))
    folder = str(month) + '月'
    os.mkdir(folder)
    os.chdir(folder)
    login();
    #num = get_num(target_url)
    num = 20180001 + month * 100
    pages = int(input('请输入你想查找的天数'))
    for i in range(pages):
        get_img('https://www.pixiv.net/ranking.php?mode=daily&date='+str(num))
        time.sleep(2)
        num += 1

if __name__ == '__main__':
    main()
