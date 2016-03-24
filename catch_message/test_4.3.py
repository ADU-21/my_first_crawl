# -*- coding:utf-8 -*-
#并发优化,实现一百个线程并发
#调整跳出循环判断条件
import urllib.request,re,sqlite3,time,gevent
from bs4 import BeautifulSoup
from gevent import monkey
monkey.patch_socket()
monkey.patch_time()

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

uurl = 'https://www.hack-cn.com/snapshot.php?p='
L = []#同时启动多个线程
for i in range(100):
    L.append(i+25)
#uid = 436820
#取出第一页第一条数据id
page_url = 'https://www.hack-cn.com/?page=1'
req = urllib.request.urlopen(page_url)
html = req.read()
#print(html)
key = r'snapshot.+View'.encode('utf8')
math = re.compile(key)
info = re.findall(math,html)
lim = int(info[0][15:21])
print(lim)

def catch(uid):
    while uid <= lim:
        try:
            view_url = uurl + str(uid)
            print('正在爬取...'+view_url)
            req = urllib.request.urlopen(view_url,timeout=10)#设置超时处理
            html = req.read()
        except Exception :
            print("请求超时,写入事务")
            con.commit()
        key = r'href="javascript:g.+'.encode('utf8')
        math = re.compile(key)
        info = re.findall(math,html)
        #print(info[0])
        i = str(info[0])
        qe = re.findall(r'[\d.]+',i)
        try:
            ipp = qe[0]#使用re获取serverIP
        except Exception:
            print("出现空白,跳过并写入事务")
            con.commit()
            uid += 100
            continue
        try:
            req = urllib.request.urlopen(view_url)
            html = req.read()
        except Exception:
            print("程序终止,写入事务")
            con.commit()
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
        insert_sql = "insert into staff (date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?)"
        cur.execute(insert_sql,(date,notifier,domain,grounds,team,ipp,server,intrusion,contact))
        uid += 100
    #执行事务
    con.commit()
    print("不要走开,广告之后马上回来...")
    time.sleep(600)
    catch(uid)

try:
    #加入gevent
    gevent.joinall([gevent.spawn(catch,uid) for uid in L])
except Exception:
    print("anything wrong")
    print(str(Exception))


cur.close()
con.close()
print("gameover")