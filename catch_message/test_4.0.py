# -*- coding:utf-8 -*-
#并发

import urllib.request,re,sqlite3,time,gevent
from bs4 import BeautifulSoup
from gevent import monkey; monkey.patch_all()

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
uid1 = 25
uid2 = 26
uid3 = 27

#uid = 436820
def catch(uid):
    while True:
        view_url = uurl + str(uid)
        print('正在爬取...'+view_url)
        req = urllib.request.urlopen(view_url)
        html = req.read()
        key = r'href="javascript:g.+'.encode('utf8')
        math = re.compile(key)
        info = re.findall(math,html)
        #print(info[0])
        i = str(info[0])
        qe = re.findall(r'[\d.]+',i)
        try:
            ipp = qe[0]#使用re获取serverIP
        except Exception:
            con.commit()
            break
        req = urllib.request.urlopen(view_url)
        html = req.read()
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
        uid += 3
    #执行事务
    con.commit()
    print("不要走开,广告之后马上回来...")
    time.sleep(5)
    catch(uid)
#catch(uid)
gevent.joinall([
        gevent.spawn(catch, uid1),
        gevent.spawn(catch, uid2),
        gevent.spawn(catch, uid3),
])


#查询记录
select_sql = "select * from staff"
cur.execute(select_sql)

#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
  print(row)

cur.close()
con.close()