'''
自动识别抽奖
直播间互动区 “关键字”出现次数>4 时，弹窗提示开始抽奖
前期准备工作需要安装：Python环境，opencv，pillow，ADB并配置好环境变量，百度文本识别

'''

#coding:utf8
import os
from PIL import Image
#import pytesseract
import cv2
import ctypes
from aip import AipOcr


def get_screen():
    os.system('adb shell screencap -p /sdcard/autolottery.png')
    os.system('adb pull /sdcard/autolottery.png ./img')
   
   
def extract_text():
    # 反阈值化，阈值为：215
    image = cv2.imread("img/textarea.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (T, threshInv) = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('img/textextract.png', threshInv)
    

def cut_image():
    # 裁出文字识别区
    image = Image.open('img/autolottery.png')
    box1 = (0, 1100, 800, 1700) # 设置图像裁剪区域(left, upper, right, lower)
    image1 = image.crop(box1)
    image1.save('img/textarea.png')
    
'''
def ocr_text():
    # 文本识别pytesseract，准确度底，弃用
    image = Image.open('img/textextract.png')
    tessdata_dir_config = '--tessdata-dir "D:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
    text = pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)
    print(text)
    return text
'''

# 配置百度AipOcr
APP_ID = '11637513'
API_KEY = 'gL1FSye2D8QlcBrz2q7TQZYh'
SECRET_KEY = '2cfn2mGZWGws0mhlxmINRBprr2A9qekf'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def baidu_ocr_text():
    # 百度文本识别AipOcr
    image = open('img/textextract.png', 'rb').read()
    msg = client.basicGeneral(image)
    text = 'result:\n'
    for i in msg.get('words_result'):
        text += (i.get('words') + '\n')
    print(text)
    return text


def string_lottery(m_str, sub_str):
    count = 0
    # 第一层循环，从主字符串的第0个元素开始
    # 第二层循环，通过切片获取下标从i开始与子字符串长度一致的字符串，并与字符串比较，如果等于子字符串则count+1
    for i in range(len(m_str)-1):
        if m_str[i:i+len(sub_str)] == sub_str:
            count += 1
    return count
    
    
while 1:
    get_screen()
    cut_image()
    extract_text()
    text = baidu_ocr_text()
    string_count = string_lottery(text, "有草")
    if string_count >= 4:
        ctypes.windll.user32.MessageBoxW(0, '要抽奖了，关键词出现次数：'+str(string_count), '抽奖了', 0)
        break
