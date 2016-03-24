# -*- coding:utf-8 -*-
#链接数据库

import urllib.request,re,sqlite3


db = r"test4.db"  #pyWork目录下test.db数据库文件
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

#cur.execute("delete from staff where id < 10")
#con.commit()
#查询记录
select_sql = "select * from staff"
cur.execute(select_sql)

#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
  print(row)
'''

maxid_sql = "select max(uid) from staff"
cur.execute(maxid_sql)
max_id = int(cur.fetchone()[0])
print("max_id:")
print(max_id)
'''

cur.close()
con.close()