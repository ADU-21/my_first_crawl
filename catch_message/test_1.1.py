# -*- coding:utf-8 -*-
#将一条爬取到的数据写入数据库
import urllib.request,re,sqlite3


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
'''
insert_sql = "insert into staff (date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?)"  #?为占位符
cur.execute(insert_sql,('1992-12-12','','','','','','','Tom','New York'))
cur.execute(insert_sql,('1992-12-12','','','','','','','Frank','Los Angeles'))
cur.execute(insert_sql,('1992-12-12','','','','','','','Kate','Chicago'))
cur.execute(insert_sql,('1992-12-12','','','','','','','Thomas','Houston'))
cur.execute(insert_sql,('1992-12-12','','','','','','','Sam','Philadelphia'))
'''
hack_url = 'https://www.hack-cn.com/?page='
page = 1
while page < 3:
    url = hack_url + str(page)
    #print(url)
    req = urllib.request.urlopen(url)
    html = req.read()
    #print(html)
    key = r'16%">.+[\u4e00-\u9fa5]+'.encode('utf8')
    math = re.compile(key)
    info = re.findall(math,html)
    for i in info:
        date = i[5:15].decode("utf8")

        insert_sql = "insert into staff (date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?)"
        cur.execute(insert_sql,(date,'','','','','','','',''))

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