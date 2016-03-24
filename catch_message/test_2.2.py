# -*-coding:utf8-*-
#获取ip
import urllib.request,re,sqlite3
from bs4 import BeautifulSoup

view_url = 'https://www.hack-cn.com/snapshot.php?p=436657'
req = urllib.request.urlopen(view_url)
html = req.read()
key = r'href="javascript:g.+'.encode('utf8')
math = re.compile(key)
info = re.findall(math,html)
#print(info[0])
i = str(info[0])
qe = re.findall(r'[\d.]+',i)
ipp = qe[0]
print(ipp)