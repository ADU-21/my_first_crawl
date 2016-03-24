# -*-coding:utf8-*-
from bs4 import BeautifulSoup
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html)
#print(soup.prettify())#格式化输出
#print(soup.a.attrs)#列表输出标签元素
#print(soup.a.get('href'))#获取标签单独元素
#print(soup.p.string)#输出标签内文字
#print(soup.head.contents[0])#列表形式输出子节点内容
#for string in soup.stripped_strings:
#    print(repr(string))#遍历取出文本中string内容
for sibling in soup.a.next_siblings:
    print(repr(sibling))