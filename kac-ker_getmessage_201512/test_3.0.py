# -*- coding:utf-8 -*-
#优化代码
#已实现静态爬取功能
import urllib.request,re,sqlite3
from bs4 import BeautifulSoup

db = r"test.db"  #pyWork目录下test.db数据库文件
drp_tb_sql = "drop table if exists staff"
crt_tb_sql = """
create table if not exists staff(
  id integer primary key autoincrement unique not null,
  uid varchar(100),
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
hack_url = 'http://hac-ker.net/?page='#一级url
page = 1
while page < 3:#修改page可更改爬取页数
    page_url = hack_url + str(page)
    #print(url)
    try:
        req = urllib.request.urlopen(page_url)
        html = req.read()#读取一级页面
        #print(html)
        key = r'snapshot.+查看快照'.encode('utf8')#找到View二级页面链接
        math = re.compile(key)
        info = re.findall(math,html)
    except Exception:
        print(Exception)
        #print(1)
    for v in info:
        id = v.decode("utf8")
        #print(id[15:-22])
        view_url = 'http://hac-ker.net/snapshot.php?p='+id[15:-22]#二级页面
        print('正在爬取...'+view_url)
        try:
            req = urllib.request.urlopen(view_url)
            html = req.read()
        except Exception:
            print(Exception)
            #print(2)
        if html.len() > 2000:
            continue
        else:
            time.wait()
        soup = BeautifulSoup(html)#使用BeautifulSoup获取信息
        h = soup.select('td[bgcolor="#FFFFFF"]')
        soup = BeautifulSoup(str(h[0]))
        L = []
        for string in soup.stripped_strings:
            L.append(string)#将获取到的信息装入List
        #分别给信息赋值
        uid = id[15:21]
        notifier = L[1]
        grounds = L[3]
        team = L[5]
        date = L[7]
        ipp = L[9]
        soup = BeautifulSoup(str(h[12]))
        server = soup.string
        soup = BeautifulSoup(str(h[14]))
        intrusion = soup.string
        soup = BeautifulSoup(str(h[16]))
        contact = soup.string
        soup = BeautifulSoup(str(h[18]))
        domain = soup.string
        #插入数据库
        try:
            insert_sql = "insert into staff (uid,date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?,?)"
            cur.execute(insert_sql,(uid,date,notifier,domain,grounds,team,ipp,server,intrusion,contact))
        except Exception:
            print(Exception)
            con.commit()
            cur.close()
            con.close()
            #print(3)
    page += 1
#执行事务
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