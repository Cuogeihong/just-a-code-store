#从百度上爬取某关键词且某一分辨率的大图

import urllib.request
from PIL import Image
from io import BytesIO
import requests
import re
import os

global i
i = 1

def post(youwant):
    global i
    params ={
                'tn' : 'resultjson_com',
                'ipn' : 'rj',
                'ct' : '201326592',
                'is' : '' ,
                'fp' : 'result',
                'queryWord' : youwant,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': '', 
                'z': '',  
                'ic': '', 
                'word': youwant,
                's' : '',
                'se' : '', 
                'tab' : '',
                'width' : '',
                'height' : '',  
                'face' : '',
                'istype' : '', 
                'qc' : '',
                'nc' : '',
                'fr' : '',
                'pn': i * 30,
                'rn': 30,
                'gsm': 'b4',
                '1535786318319' : '' 
            } 
    i += 1        
    url = 'https://image.baidu.com/search/acjson'
    req = ''
    try:
        req = requests.get(url, params = params).json().get('data')
    except:
        print('Something is wrong!!!')    
    return req        

def main():
    folder = input('给你的文件夹起个名吧: ')
    os.mkdir(folder)
    os.chdir(folder)
    youwant = input("输入你想查找的图片: ")
    num = int(input("输入你想查找的图片个数: "))
    acnum = 0
    resolution = input('输入分辨率，请在两个数字之间使用空格: ').split()
    leng = int(resolution[0])
    width = int(resolution[1])
    sum = 1  
    while acnum < num:
        reqs = post(youwant)
        if len(reqs) == 0:
            continue 
        for j in reqs:
            try:
                if 'replaceUrl' in j and 'ObjURL' in j['replaceUrl'][1]:
                    url = j['replaceUrl'][1]['ObjURL']
                    refer = j['replaceUrl'][1]['FromURL']
                    judge = url[-4:]
                    print(judge)
                    if judge[0] != '.' and judge[1] != 'j':
                        continue 
                    header = {
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                        'Referer' : refer
                    }
                    print(url)
                    print(refer)
                    req = urllib.request.Request(url, headers = header)
                    try:
                        respose = urllib.request.urlopen(req, timeout = 5)
                    except:
                        continue    
                    html = respose.read()
                    im = Image.open(BytesIO(html)) 
                    size = im.size
                    print(size)
                    if size[1] != width or size[0] != leng:
                        continue      
                    file = str(sum) + url[-4:]
                    print(file)
                    f = open(file,'wb')
                    f.write(html)
                    sum += 1
                    acnum += 1
            except:        
                print("出错啦！！")  

if __name__ == '__main__':
    main()