#coding:utf-8
__author__ = 'huafeng'
import re
import os
import requests
import codecs
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
        # print len(msg_list)
        topic_url_list = [BeautifulSoup(item).find('a')['href'] for item in msg_list]
        # print topic_url_list
        total_topic_id_set |= set(topic_url_list)
    print len(total_topic_id_set)
# post_to_get_topic_id()

def get_questions_by_topic_id():
    url = 'http://www.zhihu.com/topic/19553298/top-answers?page=1'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    #话题标签
    category_name = soup.find('h1', class_='zm-editable-content')
    print category_name

    #该url下所有的问题
    div_level_list = soup.find_all('div', class_='content')#该topic下的所有问题
    print len(div_level_list)

    #该topic下第一个问题的相关信息
    div_content = div_level_list[0]
    div_content.h2.a['href'] = 'http://www.zhihu.com' + div_content.h2.a['href']
    answer_title = div_content.h2
    answer_vote_count = div_content.find('a', class_='zm-item-vote-count')
    answer_content = div_content.find('div', class_='zm-item-rich-text')
    #由BeautifulSoup对象转化为html字符串
    answer_title = str(answer_title).decode('utf-8')
    answer_vote_count = str(answer_vote_count).decode('utf-8')
    answer_content = str(answer_content).decode('utf-8')
    # print answer_title
    # print answer_vote_count
    # return title, vote_count, answer_content
# get_questions_by_topic_id()

def get_answer_by_question_id():
    url = 'http://www.zhihu.com/question/27705700'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    #html main content
    main_content = soup.find('div', class_='zu-main-content')

    #问题title
    question_title = main_content.find('div', id='zh-question-title')
    print question_title
    #问题内容描述
    question_detail = main_content.find('div', id='zh-question-detail')
    print question_detail

    #某一回答内容
    answer_item = main_content.find('div', class_='zm-item-answer')
    # print answer_item
    #赞同数量
    vote_count = answer_item.find('span', class_='count')
    print vote_count
    #评论数
    commant_count = answer_item.find('a', class_=' meta-item toggle-comment')
    print commant_count
    #回答的具体内容
    answer_item_content = answer_item.find('div', class_='zm-item-rich-text')
    print '*'*30
    print answer_item_content
    # return str(answer_item_content).decode('utf-8')
    #答案aid
    data_aid = answer_item['data-aid']
    print data_aid, '##########'

# get_answer_by_question_id()

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

def call_error_url():
    url = 'http://www.zhihu.com/topic/19555542/top-answers?page=36'
    r = requests.get(url)
    print r.status_code == 404
# call_error_url()

def send_question_content_to_email():
    import mail_send
    mail_content_list = []
    filename = os.path.join('question_json_data.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        count = 0
        for line in f.readlines():#5837
            count += 1
            json_data = json.loads(line)
            title = json_data['title']
            content = json_data['content']
            mail_content_list.append(title + content)
            if count % 20 == 0:
                mail_send.send_email_to_evernote(''.join(mail_content_list))
                print count
                mail_content_list =  []
# send_question_content_to_email()
def convert_to_html_pattern():
    '''图片信息被抓回时, 尖括号标签被表示为了: &lt; &gt;'''
    s = '&lt;img src="http://pic1.zhimg.com/173a37c02a90d9c70b764a87ccca876c_b.jpg" data-rawwidth="354" data-rawheight="107" class="content_image" width="354"&gt;'
    print s.replace('&lt;', '<').replace('&gt;', '>')

# with codecs.open('sys/questions_id_0228.txt', encoding='utf-8') as f:
#     print len(f.readlines())
# import mail_send
# with codecs.open(r'E:\github\zhihu\text_data\zhihu_v500_l100-150_d20150301.html') as f:
#     mail_send.send_to_163_mail(f.read(), 'sivilwang@163.com')
def remove_repeat():
    with codecs.open('question_id_500.txt') as f:
        line_list = f.readlines()
        print len(line_list)
        print len(set(line_list))
        codecs.open('question_id_500.txt', mode='wb').writelines(set(line_list))

def remove_all_repeat():
    '''对有所文件的id去重'''
    total_line_set = set()
    with codecs.open('./sys/all_question_id.txt') as f:
        for line in f:
            total_line_set.add(line)
    codecs.open('question_id.txt', mode='wb').writelines(total_line_set)

def splite_file():
    '''文件切割，把文件切割为N等份'''
    import split_file
    filename = 'question_answer_content_2015_05_24.txt'
    split_file.cut_file(filename, 10)

def send_file_to_163():
    import mail_send
    for file_index in range(1, 11):
        filename = 'data/question_answer_content_2015_05_24.txt.partial_%s' % file_index
        print filename

        with codecs.open(filename) as f:
            mail_send.send_to_163_mail(f.read(), 'sivilwang@163.com')
            time.sleep(10)

send_file_to_163()