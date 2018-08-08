# Python+ADB实现自动点赞和抽奖检测

#### 原文地址：[猎奇 | Python+ADB实现自动点赞和抽奖检测](https://www.baidu.com/)

## 为什么要做这个呢？
在各类直播平台，都有对主播点赞的功能，有一些直播平台（例如淘宝直播）的点赞按钮是可以无限点击的（为什么要双击666，明明可以无限击）。在淘宝直播中，主播看到自己收获很多赞之后，有概率放一些粉丝福利，某些福利是以抽奖为形式的，粉丝们在互动区疯狂发送关键字，主播随机截图，并给在截图中的粉丝送出福利。这个过程需要粉丝疯狂的点赞，以及实时盯着屏幕以防什么时候开始刷屏抽奖。如果全程亲自操作，依靠自己手动点击的话，不能解放双手，是非常拉底做事效率的。如果依靠自己盯着屏幕看，也是非常原始的做法。

所以，如果能有一个自动点赞+自动窥屏的外挂将会让我们在薅羊毛的路上满载而归。

<div align=center><img src='https://mmbiz.qpic.cn/mmbiz_png/4guYGsRdZEQsoxTmu1eoFGwDC2M6e3hI1F8AL1cGyx1qNpBqRAkJbxPP0XXKNthI5owYRqCicVpBia8s3m1VyKTw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1', width="150" alt="这是一个表情包" /></div>

鉴于之前已经有同学实现了自动挖掘抖音美女的案例，所以这个想法终于有了一丝付诸实践的曙光，潘老师和这位同学一样使用了Python+ADB的方式来实现。

Python大家都很熟悉，人生苦短，我用Python。

ADB（Android Debug Bridge）则是一种通过电脑调试控制安卓设备的技术，我可以在电脑上输入指令，达到和手工操作一样的效果（比如说我可以用电脑控制安卓手机点开某个应用，点击某个按钮等等）。仿佛开了外挂一样舒爽。

（前期准备工作需要安装：Python环境，opencv，pillow，ADB并配置好环境变量，免费注册一个百度文本识别的账号）

## 自动点赞
### 获取点击的位置

我想知道点击了屏幕之后，这个点的位置是多少，该如何操作？

首先连接电脑与手机，手机打开USB调试，接着在电脑上打开cmd输入
```c
adb shell getevent
```
这时cmd会等待点击。

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/1.PNG' /></div>

我点击了键盘上a字母的位置，cmd给出了以下信息。找到下面的信息，最后括号位置的十六进制数就是坐标，换算成十进制即可。
```c
/dev/input/event4: 0003 0035 (X坐标)
/dev/input/event4: 0003 0036 (Y坐标)
```

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/2.PNG' /></div>

### 自动点赞

首先，ADB语句控制点击屏幕上某一点的指令是：
```c
adb shell input tap 123 456
```
其中的123 456是点击位置的坐标，这个坐标可以通过上一节方式获取。经过测试，淘宝直播的右下角点赞按钮坐标大概是(1015, 1730)。

为了避免让淘宝觉得这个操作太机器人，所以不让他每次都点击到这个固定点，让他随机出现一个偏移（虽然仔细想想好像这样做也没什么意义）。

为了一直点下去，加一个循环进去，使用for循环，可以指定给主播点多少个赞。同样地，为了不让淘宝觉得点击速度太均匀，加入一个随机的延迟。点赞主要的部分就是如下代码了：
```python
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
```
实际测试一下，我们先使用这个方法点一点键盘上的a字母看看：

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/3.PNG' /></div>

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/4.png', width=480 /></div>

嗯还是可以的。

## 检测有没有抽奖
### 获取屏幕

ADB截取屏幕的指令是：
```c
adb shell screencap -p /sdcard/autolottery.png
```
其中-p后面接的是存放的路径和文件名。

ADB把文件从手机中拷贝出来的指令是：
```c
adb pull /sdcard/autolottery.png ./img
```
第一个路径是手机中文件的路径和文件名，后一个路径是存放在电脑中的路径，./img表示存在当前py文件目录下的img文件夹里。

在python中给Android发送ADB指令则通过调用系统cmd实现，让python帮你把引号里面的句子输进cmd并且执行：
```python
def get_screen():
    os.system('adb shell screencap -p /sdcard/autolottery.png')
    os.system('adb pull /sdcard/autolottery.png ./img')
```

### 截图预处理

由于直接拿来截图进行文本识别，正确率较低（经过测试实际是非常低了），所以需要对源图像处理一下。这里需要安装opencv和pillow。

首先裁剪出文本区域，尽量去除干扰。
```python
import cv2
from PIL import Image

def cut_image():
    # 裁出文字识别区
    image = Image.open('img/autolottery.png')
    box1 = (0, 1100, 800, 1700) #设置图像裁剪区域(left, upper, right, lower)
    image1 = image.crop(box1)
    image1.save('img/textarea.png')
```
然后将该区域二值化，提升识别率，由于要识别的文字部分颜色是纯白，所以阈值可以设的大一些：
```python
def extract_text():
    # 图像分割
    image = cv2.imread("img/textarea.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # 转灰度图
    (T, threshInv) = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY_INV) # 反阈值化，阈值为215
    cv2.imwrite('img/textextract.png', threshInv)
```
原图：

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/5.png', width=480 /></div>

处理后：

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/6.png', width=480 /></div>

### 文本识别

二话不说，直接怼百度的文本识别。百度毕竟是汉语起家，识别汉语的准确度还是很高的。
```python
from aip import AipOcr
# 配置百度AipOcr
APP_ID = '自己去注册'
API_KEY = '自己去注册'
SECRET_KEY = '自己去注册'

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
```
看一下识别上面图片的结果：

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/7.PNG' /></div>

在识别简体中文的同时，不耽误识别数字，实际上识别中文的同时英文字母也可以识别但是准确率低一些。

### 字符串与子串

这种基本算法（虽说潘老师算法很渣）就不需要解释很多了，送分题。
```python
def string_lottery(m_str, sub_str):
    count = 0
    # 第一层循环，从主字符串的第0个元素开始
    # 第二层循环，通过切片获取下标从i开始与子字符串长度一致的字符串，并与字符串比较，如果等于子字符串则count+1
    for i in range(len(m_str)-1):
        if m_str[i:i+len(sub_str)] == sub_str:
            count += 1
    return count
```

### 组装

当我们有了获取屏幕，并且识别其中文本的能力，那就让他自动为我们检测有没有出现抽奖契机，根据经验，如果屏幕中有4条以上抽奖关键字，证明抽奖要开始了，大家已经躁动起来了，所以要让刚刚识别出的那串文本里出现“指定关键字”这个子字符串数量大于等于4即可。

直接怼，不解释：
```python
import ctypes

while 1:
    get_screen()
    cut_image()
    extract_text()
    text = baidu_ocr_text()
    string_count = string_lottery(text, "抽奖")
    if string_count >= 4:
        ctypes.windll.user32.MessageBoxW(0, '要抽奖了，关键词出现次数：'
             + str(string_count), '抽奖了', 0)
        break
```
因为目前时间主播还没有开播，所以先自己拿备忘录打几个字试试。

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/8.png', width=480 /></div>

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/9.PNG' /></div>

## 实际测试
可悲的事情发生了，测试的时候发现主播已经调整了抽奖方式，多数奖品用随机放出的“狂戳福利按钮”送出了，晚上只出了一次刷屏抽奖的方法。所以，这件事情告诉我们，**产品研发就是在和时间赛跑。**

所以，下次开发自动检测“狂戳福利按钮”并自动狂戳的外挂？

实际测试效果（关键字：“有草”）：

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/11.png', width=800 /></div>

<div align=center><img src='https://github.com/divertingPan/Auto_Lottery/blob/master/screenshot/10.PNG' /></div>

在这个外挂的辅助下，潘老师还是没有抽到奖，也许这就是，非命不改。

<div align=center><img src='https://mmbiz.qpic.cn/mmbiz_png/4guYGsRdZEQsoxTmu1eoFGwDC2M6e3hImiaaRxtcOgThtyhJC4pa30riaR6CQ3OjXl5NfQia78LpzaRhMheMCwo2g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1', width="150" alt="这是一个表情包" /></div>

## 总结

~~运气差这种事，用python都拯救不了。~~

---

其实单看这个外挂还是有很多成长空间的，例如：

【点赞】可以先检测用户点击的坐标，接受并传递给代码里的坐标。节省事先查坐标的时间和精力。

【抽奖】可以改造关键字的部分，不需要手动指定关键字，智能识别刷屏的字符串。再者还可以添加自动打字参与刷屏，以及自动检测抽奖结果，实现全自动无人值守式抽奖。
