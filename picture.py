#瞎写 
#图片的简易缩略图

from PIL import Image
import os
import numpy as np
import math
import colorsys

leng = 800
width = 600
div_num = 200
img_num = 138
div_leng = 4
div_width = 3

def divide(im, im_aim, name):
    ans = []
    aim = []
    answer = []
    print("正在进行参考图片的分析")  
    print("共需完成%d部分分析" % (img_num))
    count_num = 0
    percent = 1
#    for i in range(0, div_num):
#        for j in range(0, div_num):
    for each in im:
        count_num += 1 
        i = 0
        j = 0 
        ans.append(calcul(i, j, each))
#        if(count_num == percent * 13800):
#            print("已完成%d%%部分参考图片的分析" % percent)
#            percent += 1             
    print("已完成参考图片的分析")           
    print("正在进行目标图片的分析与匹配")   
    print("共需完成%d部分分析" % (div_num*div_num))
    count_num = 0
    for i in range(0, div_num):
        for j in range(0, div_num):   
            count_num += 1     
            aim = calcul(i, j, im_aim)
           # print(aim)
            answer.append(compare(aim, ans))
            if count_num == percent * div_num * div_num / 100:
                print("已完成%d%%部分目标图片的分析匹配" % percent)
                percent += 1
            
    print("正在打印图片")        
    contect(im, answer, name)   
    return 

def get_main_color(image):
    max_score = -1
    main_color = None
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):
        s = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
        y = (y-16.0)/(235-16)
        #if y > 0.9:
         #   continue
        score = (s+0.1)*count
        if score > max_score:
            max_score = score
            main_color = [r, g, b]
  #  print(main_color)        
    return main_color

def calcul(x, y, each):
    image = each.crop((x*div_leng, y*div_width, x*div_leng + div_leng, y*div_width + div_width))
    return get_main_color(image)       

def get_dis(lis1, lis2):
    r1 = lis1[0]
    g1 = lis1[1]
    b1 = lis1[2]
    r2 = lis2[0]
    g2 = lis2[1]
    b2 = lis2[2]
    rmean = (r1 + r2) / 2
    r = r1 - r2
    g = g1 - g2
    b = b1 - b2
    return math.sqrt((2+rmean/256)*(r**2)+4*(g**2)+(2+(255-rmean)/256)*(b**2))

def compare(aim, ans):
    minn = 99999.0
    min_data = -1
    i = 0
    for each in ans:
 #       print(type(each))
        temp = get_dis(aim, each)
        if temp < minn:
            minn = temp
            min_data = i
        i += 1    

    return min_data

def contect(im, answer, name):
    count = 0
    newIm = Image.new('RGB', (leng, width))
    for i in range(0, leng, div_leng):
        for j in range(0, width, div_width):
            temp = answer[count]
            t = temp % img_num
            temp /= img_num
            y = temp % div_num
            x = temp / div_num
            cutIm = im[t].crop((x, y, x + div_leng, y + div_width))
            newIm.paste(cutIm, (i, j))
            count += 1
    newIm.save('E:\\jobs\\python\\nature\\ans_' + name)
    return

def main():
    name = input('输入图片名称，包括拓展名: ')
    im_aim = Image.open('E:\\jobs\\python\\nature\\' + name)
    im = []
    for i in range(1, 1 + img_num):
        im.append(Image.open('E:\\jobs\\python\\color\\'+str(i)+'.jpg'))
    divide(im, im_aim, name)    

if __name__ == '__main__':
    main()