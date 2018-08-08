'''
测试：点击键盘a
'''

#coding=utf8
import os
import time
import random


def click_hearts(i):
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    randomX = str(random.randint(-2, 2) + 96)
    randomY = str(random.randint(-2, 2) + 1372)
    cmd = 'adb shell input tap ' + randomX + ' ' + randomY
    os.popen(cmd)
    print('%s%d, %s%f%s, %s(%s,%s)'%('已点赞 X', i, '延迟', delay, 's',
          '点击坐标：', randomX, randomY))
    
          
for i in range(1,21): # 自动点赞20次
    click_hearts(i)
    