import urllib.request
import os
import base64
import hashlib
import re

def _md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    return m.hexdigest()

def _base64_decode(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data)

def get_imgurl(m, r='', d=0):
 #   print(m)
    d = str(m[:])
 #   print(r)
 #   m='Ly93eDQuc2luYWltZy5jbi9tdzYwMC8wMDY3MUtZbmd5MWZyd2t2cG9oeXNqMzBnMDBzZ2Robi5qcGc='
 #   e = "DECODE"
    '''
    q = 4
    r = _md5(r)
    o = _md5(r[0:0 + 16])
    n = _md5(r[16:16 + 16])
    l = m[0:q]
    c = o + _md5(o + l)
    m = m[q:]
    '''
    '''
 #   print(m)
    k = _base64_decode(m)
 #   print(k)
    h = list(range(256))
    b = [ord(c[g % len(c)]) for g in range(256)]

    f = 0
    for g in range(0, 256):
        f = (f + h[g] + b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp

    t = ""
    p, f = 0, 0
    for g in range(0, len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        t += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    t = t[26:]
    '''
    print(d)
    if(d.find('gif') != -1):
        return
    iu = base64. urlsafe_b64decode(d)
    iu = str(iu)
    iu = 'http:'+iu[2:-1]
    print(iu)
    save_imgs(iu)
    return

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    respose = urllib.request.urlopen(req)
    html = respose.read()
    return html

def get_page(url):
    html = url_open(url).decode('utf-8')

    a= html.find('Older Comments')+45
    b= html.find('#comments',a)
    return html[a:b]

def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addr = []
    
    js_url = 'http:' + re.findall('<script src="(//cdn\.jandan\.net/static/min/[\d|\w]*\.\d*\.js)"></script>', html)[-1]
    js = url_open(js_url).decode('utf-8')
    r = re.findall('c=[\w\d]+\(e,"(.*?)"\)',js)[0]
        
    a = html.find('/><span class="img-hash">')+25
    while a!=-1:
        b = html.find('</span></p>',a)
        if b!=-1:
            m = html[a:b]
            if(m.find('r="ltr" lang="zh">') != -1):
                return
            get_imgurl(m, r)
        else:
            b = a
        a = html.find('/><span class="img-hash">',b)+25  
    

def save_imgs(each):
    filename = each.split('/')[-1]
    f = open(filename,'wb')
    img = url_open(each)
    f.write(img)

def main(folder='jiandan', pages=100 ):
    pages = int(input("请输入你想查找的页数"))
    os.mkdir(folder)
    os.chdir(folder)
    url = 'http://jandan.net/ooxx/'
    page_num = int(get_page(url))

    for i in range(pages):
        print(i)
        page_num -= 1
        page_url = url + 'page-' + str(page_num) + '#comments'
        find_imgs(page_url)
        
if __name__ == '__main__':
    main()
