# -*- coding:utf-8 -*-
#并发2
import re,sqlite3,time,gevent
from bs4 import BeautifulSoup
from gevent import monkey
import requests

session = requests.session()
monkey.patch_socket()
monkey.patch_time()

db = r"test4.db"  #pyWork目录下test.db数据库文件
drp_tb_sql = "drop table if exists staff"
crt_tb_sql = """
create table if not exists staff(
  id integer primary key autoincrement unique not null,
  uid int,
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
#cur.execute(drp_tb_sql)
cur.execute(crt_tb_sql)
insert_sql = "insert into staff (uid) values (?)"
cur.execute(insert_sql,('0'))


L = []
uid = 25
for i in range(10):
    L.append(uid+i)
#取出第一页第一条数据id
page_url = 'https://www.hack-cn.com/?page=1'
html = session.get(page_url).text.encode('utf8')
key = r'snapshot.+View'.encode('utf8')
math = re.compile(key)
info = re.findall(math,html)
lim = int(info[0][15:21])

def catch(uid):
    uurl = 'https://www.hack-cn.com/snapshot.php?p='
    try:
        view_url = uurl + str(uid)
        print(view_url)
        html = session.get(view_url,timeout=10).text.encode('utf8')#设置超时处理

    except Exception :
        print("请求超时")
        return
    key = r'href="javascript:g.+'.encode('utf8')
    math = re.compile(key)
    info = re.findall(math,html)
    #print(info[0])
    i = str(info[0])
    qe = re.findall(r'[\d.]+',i)
    try:
        ipp = qe[0]#使用re获取serverIP
    except Exception:
        print("出现空白,执行跳过")
        return
    try:
        html = session.get(view_url).text.encode('utf8')
    except Exception:
        print("程序终止")
        return
    soup = BeautifulSoup(html)#使用BeautifulSoup获取剩下信息
    h = soup.select('td[bgcolor="#FFFFFF"]')
    soup = BeautifulSoup(str(h[0]))
    L = []
    for string in soup.stripped_strings:
        L.append(string)#将获取到的信息装入List
    #分别给信息赋值
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
    #插入数据库
    insert_sql = "insert into staff (uid,date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?,?)"
    cur.execute(insert_sql,(uid,date,notifier,domain,grounds,team,ipp,server,intrusion,contact))
    print("写入一条数据")

#下一轮uid中最小值大于数据库里最大的值
while uid < lim:
    #获取数据库里最大id
    maxid_sql = "select max(uid) from staff"
    cur.execute(maxid_sql)
    max_id = int(cur.fetchone()[0])
    print("max_id:")
    print(max_id)
    L= []
    for i in range(10):
        L.append(uid+i)
    if uid > max_id:
        #并发写入数据
        gevent.joinall([gevent.spawn(catch,uid) for uid in L])
        print("执行事务")
        con.commit()
        uid += 10
    else: uid += 10

cur.close()
con.close()