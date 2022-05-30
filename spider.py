# -*- coding = utf-8 -*-
# @Time : 2021/8/17 13:13
# @File : spider.py
# @Software : PyCharm
import re
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import xlwt
import pymysql

findLink = re.compile(r'<a href="(.*?)">')  # 生成正则表达式
# 图片规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S
# 片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 概述
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)
        # 解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []  # 保存一部电影的信息
            item = str(item)
            # 影片详情链接
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  # 留空外文名
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
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            data.append(bd.strip())  # 去除前后空格
            datalist.append(data)  # 处理好一部电影信息
    print(datalist)
    return datalist


def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片英文名", "评分", "评价数", "概述", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % i)
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])

    book.save(savepath)


def saveDataDB(datalist, dbpath):
    conn = pymysql.connect(host='localhost', user='root', password='@@@123', database='jdbc')
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250 (
            info_link, pic_link, cname, ename, score, rated, introduction, info) 
            values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
# def init_db(dbpath):
#     sql = '''
#         create table movie250
#         (
#         id integer primary key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar,
#         score decimal ,
#         rated decimal ,
#         introduction text,
#         info text
#         )
#     '''
#     conn = pymysql.connect(host="localhost", user="root", password="root", database="jdbc", port=3306)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    # # savepath = "豆瓣电影Top250.xls"
    dbpath = "movie250.db"
    saveDataDB(datalist, dbpath)
    # askURL("https://movie.douban.com/top250?start=0")


def askURL(url):
    headers = {
        "User-Agent": "Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 92.0.4515.159 Safari / 537.36"
    }
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":
    main()
