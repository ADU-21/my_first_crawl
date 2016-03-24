# -*- coding:utf-8 -*-
#优化代码
#更新数据库
import urllib.request,re,sqlite3,time
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
'''
#创建表staff
cur.execute(drp_tb_sql)
cur.execute(crt_tb_sql)
'''
#插入记录
hack_url = 'http://hac-ker.net/?page='#一级url
def catch(url):
    page = 1
    while page > 0:#爬取所有网页
        page_url = hack_url + str(page)
        #print(url)
        req = urllib.request.urlopen(page_url)
        html = req.read()#读取一级页面
        #print(html)
        key = r'snapshot.+查看快照'.encode('utf8')#找到View二级页面链接
        math = re.compile(key)
        info = re.findall(math,html)
        #比对更新id与数据库里原有id
        maxid_sql = "select max(uid) from staff"
        cur.execute(maxid_sql)
        max_id = int(cur.fetchone()[0])
        for v in info:
            id = v.decode("utf8")
            #print(id[15:-22])
            view_url = 'http://hac-ker.net/snapshot.php?p='+id[15:-22]#二级页面
            print('正在爬取...'+view_url)
            req = urllib.request.urlopen(view_url)
            html = req.read()
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
            print(max_id)
            print(uid)
            if int(uid) > max_id:
                try:
                    #插入数据库
                    insert_sql = "insert into staff (uid,date,notifier,domain,grounds,team,serverIP,server,intrusions,contact) values (?,?,?,?,?,?,?,?,?,?)"
                    cur.execute(insert_sql,(uid,date,notifier,domain,grounds,team,ipp,server,intrusion,contact))
                    print("插入一条数据:")
                    print(uid,date,notifier,domain,grounds,team,ipp,server,intrusion,contact)
                    #continue
                except Exception:
                    print(Exception)
                #continue
            else:
                print("执行事务")
                con.commit()
                print('当前未出现更新数据...5s后自动刷新')
                time.sleep(5)
                catch(url)
                '''
                #更新最大id
                maxid_sql = "select max(uid) from staff"
                cur.execute(maxid_sql)
                max_id = int(cur.fetchone()[0])
                print('当前未出现更新数据...5s后自动刷新')
                #print(max_id)
                time.sleep(5)
                '''

        page += 1


catch(hack_url)
#执行事务
#con.commit()

'''
#查询记录
select_sql = "select * from staff"
cur.execute(select_sql)

#返回一个list，list中的对象类型为tuple（元组）
date_set = cur.fetchall()
for row in date_set:
  print(row)
'''
cur.close()
con.close()