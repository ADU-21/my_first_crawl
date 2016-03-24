# -*-coding:utf8-*-
#遍历所有要爬取的网页
import urllib.request,re,sqlite3

hack_url = 'https://www.hack-cn.com/?page='
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
        print(view_url)

    page += 1

    #<a href="snapshot.php?p=436656" target="_blank">View</a>
    #https://www.hack-cn.com/snapshot.php?p=436656