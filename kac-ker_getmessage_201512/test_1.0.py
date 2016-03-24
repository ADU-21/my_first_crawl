# -*-coding:utf8-*-
#遍历所有要爬取的网页
import urllib.request,re,sqlite3

#取到一共多少页

hack_url = 'http://hac-ker.net/?page='
page = 1
while page < 3:
    page_url = hack_url + str(page)
    #print(url)
    req = urllib.request.urlopen(page_url)
    html = req.read()
    #print(html)
    key = r'snapshot.+查看快照'.encode('utf8')
    math = re.compile(key)
    info = re.findall(math,html)
    for v in info:
        id = v.decode("utf8")
        #print(id[15:-22])
        view_url = 'http://hac-ker.net/snapshot.php?p='+id[15:-22]
        print(view_url)

    page += 1