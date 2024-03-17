# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import time

# 开始计时
t1=time.time()
print('#'*50)

findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，标售规则   影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)




def main():
    baseurl = "https://movie.douban.com/top250?start="  #要爬取的网页链接
    # 1.爬取网页
    dataList = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"    #当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(dataList, savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist, dbpath)



def getData(baseurl):
    urls = []
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        urls.append(url)
    dataList = []
    # 引入多线程
    executor = ThreadPoolExecutor(max_workers=10)
    # submit()的参数： 第一个为函数， 之后为该函数的传入参数，允许有多个
    tasks = [executor.submit(getDataOne, url, dataList) for url in urls]
    # 等待所有的线程完成，才进入后续的执行
    wait(tasks, return_when=ALL_COMPLETED)
    return dataList

# 爬取网页
def getDataOne(url,dataList):
    html = askURL(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串
        data = []  # 保存一部电影所有信息
        item = str(item)
        link = re.findall(findLink, item)[0]  # 通过正则表达式查找
        data.append(link)
        imgSrc = re.findall(findImgSrc, item)[0]
        data.append(imgSrc)
        titles = re.findall(findTitle, item)
        if (len(titles) == 2):
            ctitle = titles[0]
            data.append(ctitle)
            otitle = titles[1].replace("/", "")  #消除转义字符
            data.append(otitle)
        else:
            data.append(titles[0])
            data.append(' ')
        rating = re.findall(findRating, item)[0]
        data.append(rating)
        judgeNum = re.findall(findJudge, item)[0]
        data.append(judgeNum)
        inq = re.findall(findInq, item)
        if len(inq) != 0:
            inq = inq[0].replace("。", "")
            data.append(inq)
        else:
            data.append(" ")
        bd = re.findall(findBd, item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
        bd = re.sub('/', "", bd)
        data.append(bd.strip())
        dataList.append(data)



# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据到表格
def saveData(dataList, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        print("第%d条" %(i+1))       #输出语句，用来测试
        print(len(dataList))
        data = dataList[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
     print("爬取完毕！")

# 结束时间
t2=time.time()
print('单线程耗时：%s' %(t2-t1))
print('#'*50)