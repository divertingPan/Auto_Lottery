'''
首先在cmd中执行 adb shell getevent 获取需要点击的位置坐标
/dev/input/event0: 0003 0035 00000341 X坐标 16进制
/dev/input/event0: 0003 0036 000008ec Y坐标 16进制

tb直播间右下角点赞坐标：(X, Y)：(1015±15, 1730±20)

'''

#coding=utf8
import os
import time
import random

def click_hearts(i):
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    randomX = str(random.randint(-15, 15) + 1015)
    randomY = str(random.randint(-20, 20) + 1730)
    cmd = 'adb shell input tap ' + randomX + ' ' + randomY
    os.popen(cmd)
    print('%s%d, %s%f%s, %s(%s,%s)'%('已点赞 X', i, '延迟', delay, 's',
          '点击坐标：', randomX, randomY))
    
for i in range(1,21): # 自动点赞20次
    click_hearts(i)