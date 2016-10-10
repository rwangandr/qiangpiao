# -*- coding:utf-8 -*-
__author__ = 'rwang'
import urllib
import request
import re
from bs4 import *

#url = 'http://zh.house.qq.com/'
#url = 'http://www.0756fang.com/'
url = 'http://www.228.com.cn/ticket-183591673.html'
html = urllib.urlopen(url).read().decode('utf-8')

soup = BeautifulSoup(html,"html.parser")
overs = soup.find_all('li',attrs={"class":"over","type":"price","zp":"333"})
#陈粒小梦大半2016巡回演唱会—天津站" p="18359
for over in overs:
    print "===",over,"==="

exit(0)
print(soup.head.meta['content'])#输出所得标签的‘’属性值
print("===")
print(soup.span.string)
print("===")
print(soup.span.text)#两个效果一样，返回标签的text
print("===")
#name属性是‘’的标签的<ResultSet>类，是一个由<Tag>组成的list
print(soup.find_all(attrs={'name':'keywords'}))

print("===")
print(soup.find_all(class_='site_name'))#class属性是‘’的<Tag>的list,即<ResultSet>

#print(soup.find_all(class_='site_name')[0])#这是一个<Tag>
print("===")
print(soup.find(attrs={'name':'keywords'}))#name属性是‘’的标签的<Tag>类
print("===")
print(soup.find('meta',attrs={'name':'keywords'}))#name属性是‘’的meta标签的<Tag>类
print("===")
print(soup.find('meta',attrs={'name':'keywords'})['content'])#<Tag类>可直接查属性值
print("===")
#配合re模块使用，可以忽略大小写
#如下面例子，可以找到name属性为keywords，KEYWORDS,KeyWORds等的meta标签
print(soup.find('meta',attrs={'name':re.compile('keywords',re.IGNORECASE)}))
exit(0)