#-*-coding:utf8-*-
#实现不用翻页遍历网页
import urllib.request,re,sqlite3
from bs4 import BeautifulSoup


uurl = 'https://www.hack-cn.com/snapshot.php?p='
uid = 25
while uid > 0:
    url = uurl + str(uid)
    req = urllib.request.urlopen(url)
    html = req.read()
    #print(html)

    uid+=1
