# -*- coding:utf-8 -*-
#合并
import urllib.request,re,sqlite3
from bs4 import BeautifulSoup

db = r"test.db"  #pyWork目录下test.db数据库文件
drp_tb_sql = "drop table if exists staff"
crt_tb_sql = """
create table if not exists staff(
  id integer primary key autoincrement unique not null,
  date varchar(100),
  notifier varchar(100),
  domain varchar(100),
  grounds varchar(100),
  team varchar(100),
  serverIP varchar(100),
  server varchar(100),
  intrusions varchar(100),
  contact varchar(100)
);
"""

#连接数据库
con = sqlite3.connect(db)
cur = con.cursor()

#创建表staff
cur.execute(drp_tb_sql)
cur.execute(crt_tb_sql)

#插入记录
hack_url = 'https://www.hack-cn.com/?page='#一级url
page = 1
while page < 3:
    page_url = hack_url + str(page)
    #print(url)
    req = urllib.request.urlopen(page_url)
    html = req.read()
    #print(html)
    key = r'snapshot.+View'.encode('utf8')
    math = re.compile(key)
    info = re.findall(math,html)
    for v in info:
        view = v.decode("utf8")
        #print(view[:21])
        view_url = 'https://www.hack-cn.com/'+view[:21]
        req = urllib.request.urlopen(view_url)
        html = req.read()
        key = r'href="javascript:g.+'.encode('utf8')
        math = re.compile(key)
        info = re.findall(math,html)
        print(info[0])
        i = str(info[0])
        qe = re.findall(r'[\d.]+',i)
        ipp = qe[0]
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
        insert_sql = "insert into staff (date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?)"
        cur.execute(insert_sql,(date,notifier,domain,grounds,team,ipp,server,intrusion,contact))

    page += 1

con.commit()

#查询记录
select_sql = "select * from staff"
cur.execute(select_sql)

#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
  print(row)

cur.close()
con.close()