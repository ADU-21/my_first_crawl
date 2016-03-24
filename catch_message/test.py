# -*-coding:utf8-*-
#爬取第一条数据
import urllib.request,re,sqlite3

hack_url = 'https://www.hack-cn.com/?page='
page = 1
while page < 3:
    url = hack_url + str(page)
    #print(url)
    req = urllib.request.urlopen(url)
    html = req.read()
    print(type(html))
    key = r'16%">.+'.encode('utf8')
    math = re.compile(key)
    info = re.findall(math,html)
    for i in info:
        date = i.decode("utf8")
        print(date)
        #notifier = i[45:67]
    page += 1
    #Notifier
'''
    key1 = r'17%">.+[\u4e00-\u9fa5]+'.encode('utf8')
    math1 = re.compile(key1)
    info1 = re.findall(math1,html)
    dict = {}
    a = 0
    for i in info:
        a += 1
        aa= i[29:].decode("utf8")
        j = re.split(r'">',aa)[0]
        dict[i] = j
    for k in dict:
    print(dict[k])'''
