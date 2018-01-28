#coding:utf8
#验证码转换，优化，优化后交给 tesserace 识别
#############
from PIL import Image

def blankToWrite(im):
    #黑白反转,im为图像对象
    pix = im.load()
    for i in range(1,im.size[0]):
        for y in range(1,im.size[1]):
            if pix[i,y] == 0:
                pix[i,y] = 255
            else:
                pix[i,y] = 0
    return im

def reNoise(im):
    #去噪点
    #value判断周围的几点是不是和这个点一样，如果这个点和周围8个点都不一样，反转
    pix = im.load()
    for i in range(2,im.size[0]-1):
        for y in range(2,im.size[1]-1):
            warp_list = [pix[i-1,y],pix[i-1,y-1],pix[i,y-1],pix[i+1,y+1],pix[i,y+1],pix[i+1,y],pix[i+1,y-1],pix[i-1,y+1],pix[i,y]]
            if  warp_list.count(pix[i,y])<3:
                if pix[i,y] == 255:
                    pix[i,y] = 0
                else:
                    pix[i,y] = 255
    return im

if __name__  == '__main__':
    im = Image.open('misc.bmp')
    reNoise(im).save('bbb.bmp')


