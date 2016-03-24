# -*-coding:utf8-*-
#解析html
import urllib.request,re,sqlite3
from bs4 import BeautifulSoup

view_url = 'https://www.hack-cn.com/snapshot.php?p=436635'
req = urllib.request.urlopen(view_url)
html = req.read()
soup = BeautifulSoup(html)
h = soup.select('td[bgcolor="#FFFFFF"]')
soup = BeautifulSoup(str(h[0]))
L = []
for string in soup.stripped_strings:
    L.append(string)

notifier = L[1]
grounds = L[3]
team = L[5]
date = L[7]
soup = BeautifulSoup(str(h[12]))
server = soup.string
soup = BeautifulSoup(str(h[14]))
intrusion = soup.string
soup = BeautifulSoup(str(h[16]))
contact = soup.string
soup = BeautifulSoup(str(h[18]))
domain = soup.string

print(notifier,grounds,team,date,server,intrusion,contact,domain)


