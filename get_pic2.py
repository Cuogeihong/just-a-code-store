import urllib.request
import requests
import re
import os

def post(youwant, num):
    params = []
    for i in range(30, 30*num + 30, 30):
        params.append(
            {
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
                'pn': i,
                'rn': 30,
                'gsm': 'b4',
                '1535786318319' : '', 
            }
        ) 
    url = 'https://image.baidu.com/search/acjson'
    reqs = []
    for each in params:
        reqs.append(requests.get(url, params = each).json().get('data'))
    return reqs        

def main():
    folder = input('给你的文件夹起个名吧')
    os.mkdir(folder)
    os.chdir(folder)
    youwant = input("输入你想查找的图片")
    num = int(input("输入你想查找的页数"))
    reqs = post(youwant, num)
    #for each in reqs[0]:
     #   print(each['replaceUrl'][0]['ObjURL'])
    sum = 1  
    ssum = 0  
    for i in reqs:
        for j in i:
            try:
                if 'replaceUrl' in j and 'ObjURL' in j['replaceUrl'][0]:
                    ssum += 1
                    url = j['replaceUrl'][0]['ObjURL']
                    refer = j['replaceUrl'][0]['FromURL']
                    header = {
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                        'Referer' : refer
                    }
                    print(url)
                    print(refer)
                    req = urllib.request.Request(url, headers = header)
                    respose = urllib.request.urlopen(req)
                    html = respose.read()
                    file = str(sum) + url[-4:]
                    print(file)
                    sum += 1
                    f = open(file,'wb')
                    f.write(html)
            except:
                try:
                    ssum -= 1
                    print('不是大图片了。。。')
                    url = j['middleURL']
                    respose = urllib.request.urlopen(url)
                    html = respose.read()
                    file = str(sum) + url[-4:]
                    print(file)
                    sum += 1
                    f = open(file,'wb')
                    f.write(html)
                except:    
                    print("出错啦！！")  
    print(ssum)

if __name__ == '__main__':
    main()