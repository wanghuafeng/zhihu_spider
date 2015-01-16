__author__ = 'huafeng'
#coding:utf-8
import re
import time
import subprocess

html = '''<ul class="zm-topic-cat-main clearfix">
<li data-id="3324"><a href="#经济学">经济学</a></li>
<li data-id="253"><a href="#游戏">游戏</a></li>
</ul>'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html)
url_list = soup.find_all('li', attrs={'data-id':re.compile('\d+')})
print url_list
#当属性为id, class时可以使用id=True, class_=True 来获取有id, class属性的数据（text=True也可以）。
#如soup.find_all('li', id=True)
#soup.find_all('li', class_=True)
#其他属性则必须使用attrs={'data-id':True}来根据制定的属性进行过滤，例子中不能使用'data-id'=True

