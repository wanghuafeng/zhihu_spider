__author__ = 'huafeng'
#coding:utf-8
import re
import requests
import time
import json
import subprocess
from bs4 import BeautifulSoup

def parse_url_li():
    html = '''<ul class="zm-topic-cat-main clearfix">
    <li data-id="3324"><a href="#经济学">经济学</a></li>
    <li data-id="253"><a href="#游戏">游戏</a></li>
    </ul>'''
    soup = BeautifulSoup(html)
    url_list = soup.find_all('li', attrs={'data-id':re.compile('\d+')})
    print url_list
    #当属性为id, class时可以使用id=True, class_=True 来获取有id, class属性的数据（text=True也可以）。
    #如soup.find_all('li', id=True)
    #soup.find_all('li', class_=True)
    #其他属性则必须使用attrs={'data-id':True}来根据制定的属性进行过滤，例子中不能使用'data-id'=True

def request_page_url():
    url = u'http://www.zhihu.com/topics'
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', class_='zh-general-list clearfix')
    item_level_list = div_level_str.find_all('div', class_='item')
    print item_level_list
    print len(item_level_list)
    print item_level_list[0].a['href']
# request_page_url()

def post_to_get_topic_id():

    topic_url = 'http://www.zhihu.com/node/TopicsPlazzaListV2'
    total_topic_id_set = set()
    for offset_index in range(3):
        post_data = {
            'method':'next',
            'params':'{"topic_id":1027,"offset":%d,"hash_id":""}',
            '_xsrf':'9095d080aa27b6669de39a5a5eb9c439',
            }
        post_data['params'] = post_data['params'] % (offset_index*20)
        json_html = requests.post(topic_url, data=post_data).text
        json_data = json.loads(json_html)
        msg_list = json_data.get('msg')
        print len(msg_list)
        topic_url_list = [BeautifulSoup(item).find('a')['href'] for item in msg_list]
        print topic_url_list
        total_topic_id_set |= set(topic_url_list)
    print len(total_topic_id_set)
# post_to_get_topic_id()

def get_questions_by_topic_id():
    url = 'http://www.zhihu.com/topic/19553298'
    r = requests.get(url)
    html = r.text
    # print html
    soup = BeautifulSoup(html)
    div_level_list = soup.find_all('div', class_='content')
    print len(div_level_list)
    print div_level_list
get_questions_by_topic_id()

def gen_range_offset():
    for offset_index in range(3):
        post_data = {
            'method':'next',
            'params':'{"topic_id":1027,"offset":%d,"hash_id":""}',
            '_xsrf':'9095d080aa27b6669de39a5a5eb9c439',
            }
        post_data['params'] = post_data['params'] % offset_index
        print post_data
# gen_range_offset()