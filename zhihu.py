#coding:utf-8
import os
import re
import time
import json
import codecs
import requests
from bs4 import BeautifulSoup
from email_to_evernote import send_to_163_mail

PATH = os.path.dirname(os.path.abspath(__file__))

class ZhihuTopicId(object):
    '''根据文件cat_id_mapping_34中的话题，解析出所有话题对应的topic_id，并写入本地'''
    topic_root_url = 'http://www.zhihu.com/topics'#话题广场根目录
    root_url = 'http://www.zhihu.com'#根目录

    def __init__(self):
        self.chosen_id_list = []
        self._load_cat_id()

    def _load_cat_id(self):
        '''读取本地文件中不以#号开头的id信息，保存到self.chosen_id_list中'''
        filename = os.path.join(PATH, 'cat_id_mapping_34.txt')
        with codecs.open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                if not line.startswith('#'):
                    # print line.strip()
                    topic_id = line.strip().split('\t')[-1]
                    self.chosen_id_list.append(topic_id)
            print len(self.chosen_id_list)

    def log_record(self):
        '''生成log句柄，用于记录日志'''
        log_filename = time.strftime('%Y_%m_%d.log')
        log_file = os.path.join(PATH, 'log', log_filename)
        self.log = codecs.open(log_file, mode='a', encoding='utf-8')

    def gen_all_topic_url_list(self):
        '''解析根目录页面，获取所有话题url'''
        try:
            html = requests.get(self.topic_root_url).text
        except BaseException:
            print 'request time out...'
            try:
                html = requests.get(self.topic_root_url).text
            except BaseException:
                print 'request time out...'
                timeFormat = time.strftime('%Y_%m_%d_%H:%M:%S')
                self.log.write("%s--topic root url log timeed out\n"%timeFormat)
                return []
        soup = BeautifulSoup(html)
        url_str = soup.find('ul', class_="zm-topic-cat-main clearfix")
        url_li_list = url_str.find_all('li', attrs={'data-id':True})
        print url_li_list
        url_list = [(item.a.text, item['data-id']) for item in url_li_list]
        print url_list
        codecs.open('cat_id_mapping.txt', mode='wb', encoding='utf-8').writelines([('\t'.join(item) + '\n') for item in url_list])

    def get_cookie_param(self):
        '''获取cookie信息'''
        cookie = requests.get(self.topic_root_url).cookies.get('_xsrf')
        print 'cookie info: ', cookie
        return cookie

    def get_topic_id(self, cattopic_id):
        '''由cattopic_id获取topic_id，这里去zhihu默认的请求次数（3次），即每个cattopic_id对应60个topic_id(/topic/19553298)'''
        topic_url = 'http://www.zhihu.com/node/TopicsPlazzaListV2'
        total_topic_id_set = set()
        for offset_index in range(3):
            post_data = {
                'method':'next',
                'params':'{"topic_id":%s,"offset":%d,"hash_id":""}',
                '_xsrf':'9095d080aa27b6669de39a5a5eb9c439',
                }
            post_data['params'] = post_data['params'] % (cattopic_id, offset_index*20)
            # print post_data
            json_html = requests.post(topic_url, data=post_data).text
            json_data = json.loads(json_html)
            msg_list = json_data.get('msg')
            # print len(msg_list)
            topic_url_list = [BeautifulSoup(item).find('a')['href'] for item in msg_list]
            # print topic_url_list#/topic/19553298
            total_topic_id_set |= set(topic_url_list)
        print len(total_topic_id_set)
        return total_topic_id_set

    def write_all_topic_id(self):
        total_id_set = set()
        for cattopic_id in self.chosen_id_list:
            total_id_set |= self.get_topic_id(cattopic_id)
        print len(total_id_set)#1524据个人习惯过滤后，余22个标签的1014个topic_id
        codecs.open('sys/all_topic_id.txt', mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_id_set])
# if __name__ == "__main__":
#     zhihu = ZhihuTopicId()
#     start_time = time.time()
#     zhihu.write_all_topic_id()
#     print time.time() - start_time
    # def utils_test():
    #     zhihu.gen_all_topic_url_list()
    #     zhihu.get_cookie_param()
    #     zhihu.get_topic_id('1027')

#**************************获取所有点赞数超过1000的问题*********************************
# class LenAnswer(object):

def get_question_id():
    '''获取所有点赞数超过1000的问题'''
    def get_question_by_topic_id(topic_id):
        '''根据topic_id解析出vote_count大于1000的question_id,并返回'''
        topic_url_pattern = 'http://www.zhihu.com{}/top-answers?page=%s'.format(topic_id.rstrip())
        topic_question_list = []
        for page_index in range(1, 51):
            topic_url = topic_url_pattern % page_index
            #返回当前页中满足要求的question_id
            one_page_question_list = get_question_list_from_topic_url(topic_url)
            #若返回question_list为空，则停止翻页
            if not one_page_question_list:
                return topic_question_list
            topic_question_list.extend(one_page_question_list)
            # print topic_url, 'page_index:', page_index,
        # print 'topic_question_list len:', len(topic_question_list)
        return topic_question_list
    # get_question_by_topic_id('/topic/19551147')

    def _load_topic_ids():
        '''读取所有的topic_id信息'''
        filename = os.path.join(PATH, 'all_topic_id.txt')
        return codecs.open(filename, encoding='utf-8').readlines()

    def get_all_question_ids():
        '''读取本地文件中的topic_id并解析所有大于1000的question_id'''
        topic_id_list = _load_topic_ids()
        total_id_list_len = len(topic_id_list)
        # print 'total_id_list_len:', len(topic_id_list)
        all_question_id_list = []
        topic_index = 0
        for topic_id in topic_id_list:
            topic_index += 1
            print total_id_list_len, topic_index,
            topic_question_list = get_question_by_topic_id(topic_id)
            print len(topic_question_list)
            all_question_id_list.extend(topic_question_list)
        codecs.open('whole_question_id.txt', mode='wb', encoding='utf-8').writelines([item+'\n' for item in all_question_id_list])
    # get_all_question_ids()
    def remove_reqeat_ids():
        question_id_filename = os.path.join(PATH, 'whole_question_id.txt')
        with codecs.open(question_id_filename, encoding='utf-8') as f:
            line_list = f.readlines()
            line_set = set(line_list)
            print len(line_set), len(line_list)
            codecs.open('question_ids.txt', mode='wb', encoding='utf-8').writelines(line_set)
    # remove_reqeat_ids()

#**************************获取所有点赞数超过1000的问题*********************************
def get_answer_by_question_id(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)

    #html main content
    main_content = soup.find('div', class_='zu-main-content')

    #问题title,作为印象笔记的标题
    question_title_span = main_content.find('div', id='zh-question-title')

    if not hasattr(question_title_span, 'text'):
        return

    question_title = question_title_span.text

    #封装“问题title”到html标签中，写入印象笔记文本的第一行
    question_title_href = '<h3><a href="%s" target="_blank">%s</a></h3>' % (url, question_title)
    # print question_title_href
    #问题内容描述
    question_detail = main_content.find('div', id='zh-question-detail')
    question_detail = str(question_detail).decode('utf-8')

    #合并问题标题和内容
    question_info = question_title_href + question_detail

    answer_item_list = main_content.find_all('div', class_='zm-item-answer')
    # print len(answer_item_list)

    answer_content_list = []
    for answer_item in answer_item_list:
        #赞同数量
        vote_count_span = answer_item.find('span', class_='count')
        if not hasattr(vote_count_span, 'text'):
            continue
        vote_count = vote_count_span.text
        # print vote_count
        if ('K' in vote_count) or (int(vote_count) > 1000):
            #回答的具体内容
            answer_item_content = answer_item.find('div', class_='zm-item-rich-text')
            answer_content_list.append('<br>*******************vote_count:%s*********************'%vote_count)
            answer_content_list.append(str(answer_item_content).decode('utf-8'))
    # print len(answer_content_list)
    answer_contents = ''.join(answer_content_list)
    # print answer_contents
    return question_title, question_info + answer_contents
# url = 'http://www.zhihu.com/question/19568396'
# get_answer_by_question_id(url)

def write_answer():
    url_pattern = 'http://www.zhihu.com'
    filename = os.path.join(PATH, 'question_ids.txt')
    json_filename = os.path.join(PATH, 'question_json_data.txt')
    with codecs.open(filename, encoding='utf-8') as f, \
    codecs.open(json_filename, mode='wb', encoding='utf-8') as wf:
        index = 0
        for line in f.readlines():
            index += 1
            print 'question index:', index
            url = url_pattern + line.strip()
            try:
                title, question_info_content = get_answer_by_question_id(url)
                json_str = json.dumps({'title': title, 'content':question_info_content}) + '\n'
                wf.write(json_str)
            except:
                print url
                continue
            # to_evernote(title, content)
            # print 'send sucessed...'


def send_to_evernote():
    from email_to_evernote import send_email_to_evernote
    filename = os.path.join(PATH, 'question_json_data.txt')
    with codecs.open(filename, encoding='utf-8') as f:
        range_from = 0
        index = range_from
        content_list = []
        for line in f.readlines()[range_from:]:
            index += 1
            print 'index:', index
            line_json = json.loads(line.rstrip())
            content = line_json['content']
            content_list.append(content)
            print 'len(content_list):', len(content_list)
            if index % 20 == 0:
                content_20_str = ''.join(content_list)
                send_email_to_evernote(str(index), content_20_str)
                print 'sending sucess...'
                content_list = []
                # title = line_json['title']
                # content = line_json['content']
                # to_evernote(title, content)
# send_to_evernote()


def get_question_list_from_topic_url(topic_url, max_vote_count=1000):
    '''根据topic_url解析出该页面中vote_count大于max_vote_count的所有question_id'''
    question_list = []
    r = requests.get(topic_url, timeout=15)
    if r.status_code == 404:
        return []
    html = r.text
    soup = BeautifulSoup(html)

    #该url下所有的问题
    div_level_list = soup.find_all('div', class_='content')#该topic下的所有问题
    # print 'question_count of div_level_list:', len(div_level_list)
    for question_div in div_level_list:
        #该topic下第一个问题的相关信息
        question_id = question_div.h2.a['href']
        answer_vote_count = question_div.find('a', class_='zm-item-vote-count').text.strip()
        if ('K' in answer_vote_count) or (int(answer_vote_count) > max_vote_count):
            # print answer_id, answer_vote_count
            question_list.append(question_id)
            # print 'question_list len:', len(question_list)
    print question_list
    return question_list
# url = 'http://www.zhihu.com/topic/19551147/top-answers?page=2'
# get_question_list_from_topic_url(url, 1000)

def get_question_by_topic_id(topic_id, max_vote_count=1000):
    '''根据topic_id解析出vote_count大于max_vote_count的question_id,并返回'''
    topic_url_pattern = 'http://www.zhihu.com{}/top-answers?page=%s'.format(topic_id.rstrip())
    topic_question_list = []
    for page_index in range(1, 51):
        topic_url = topic_url_pattern % page_index
        #返回当前页中满足要求的question_id
        # one_page_question_list = get_question_list_from_topic_url(topic_url, max_vote_count)
        one_page_question_list = []
        r = requests.get(topic_url, timeout=15)
        #若该topic_id对应页面不存在，则返回空数组
        if r.status_code == 404:
            return []
        html = r.text
        soup = BeautifulSoup(html)
        #该topic_id对应page_index下的所有问题
        div_level_list = soup.find_all('div', class_='content')
        try:
            for question_div in div_level_list:
                #该topic下第一个问题的相关信息
                question_id = question_div.h2.a['href']
                answer_vote_count = question_div.find('a', class_='zm-item-vote-count').text.strip()
                if ('K' in answer_vote_count) or (int(answer_vote_count) > max_vote_count):
                    # print answer_id, answer_vote_count
                    one_page_question_list.append(question_id)
        except:
            print topic_url

        #若返回question_list为空，则停止翻页
        if not one_page_question_list:
            return topic_question_list
        topic_question_list.extend(one_page_question_list)
        # print topic_url, 'page_index:', page_index,
    # print 'topic_question_list len:', len(topic_question_list)
    return topic_question_list
# get_question_by_topic_id('/topic/19551147')

def _load_topic_ids():
    '''读取所有的topic_id信息'''
    filename = os.path.join(PATH, 'sys', 'all_topic_id.txt')
    return [item.rstrip() for item in codecs.open(filename, encoding='utf-8').readlines()]

def get_all_question_ids():
    '''读取本地文件中的topic_id并解析所有大于1000的question_id'''
    topic_id_list = _load_topic_ids()
    total_id_list_len = len(topic_id_list)
    # print 'total_id_list_len:', len(topic_id_list)
    all_question_id_list = []
    topic_index = 0
    for topic_id in topic_id_list:
        topic_index += 1
        print total_id_list_len, topic_index,
        topic_question_list = get_question_by_topic_id(topic_id)
        print len(topic_question_list)
        all_question_id_list.extend(topic_question_list)
    codecs.open('whole_question_id.txt', mode='wb', encoding='utf-8').writelines(set([item+'\n' for item in all_question_id_list]))
# get_all_question_ids()
#***********************humorous answer************************************
class HumorAnswer(object):
    '''获取知乎humor answer'''
    def __init__(self):
        self.total_question_id_set = set()

    def get_question_ids_by_topic_id(self, max_vote_count_limit=500, topic_id_filename=None):
        '''由topic_id(1524)解析出所有的question_id'''
        if not topic_id_filename:
            #若没有指定具体topic_id_filename，则默认为目录sys下的all_topic_id.txt
            filename = os.path.join(PATH, 'sys', 'all_topic_id.txt')
        else:
            filename = topic_id_filename
        total_topic_id_list = [item.rstrip() for item in codecs.open(filename, encoding='utf-8').readlines()]

        total_id_list_len = len(total_topic_id_list)#topic_id的数量
        topic_index = 0
        #由topic_id解析出所有question_id,去重
        for topic_id in total_topic_id_list:
            topic_index += 1
            print total_id_list_len, topic_index
            question_id_list = get_question_by_topic_id(topic_id, max_vote_count=max_vote_count_limit)
            # print len(topic_question_list)
            self.total_question_id_set |= set(question_id_list)
        print 'total_topic_question_set len is:', len(self.total_question_id_set)

    def get_humor_answer_by_question_id(self, max_vote_count_limit=500):
        '''由question_id获取answer_id'''
        zhihu_root_url = 'http://www.zhihu.com'

        #所有answer_id的集合
        answer_id_set = set([item.rstrip() for item in codecs.open('humor_Q_A_answer_id.txt', encoding='utf-8').readlines()])

        humor_Q_A_fileObj = codecs.open(time.strftime('humor_Q_A_%Y_%m_%d.txt'), mode='ab', encoding='utf-8')
        answer_id_obj = codecs.open('humor_Q_A_answer_id.txt', mode='ab', encoding='utf-8')

        #遍历question_id，获取符合要求的answer，并将对应answer_id写入本地
        self.total_question_id_set = [item.rstrip() for item in codecs.open('whole_question_id.txt', encoding='utf-8').readlines()]
        for question_id in self.total_question_id_set:
            answer_text_list = []
            answer_id_list = []
            url = zhihu_root_url + question_id
            r = requests.get(url, timeout=15)
            html = r.text
            soup = BeautifulSoup(html)
            try:
                main_content = soup.find('div', class_='zu-main-content')
                question_title = main_content.find('div', id='zh-question-title').text.strip()
                answer_item_list = main_content.find_all('div', class_='zm-item-answer')
                for answer_item in answer_item_list:
                    vote_count = answer_item.find('span', class_='count').text.strip()
                    #若点赞数大于max_vote_count_limit，则将answer_id写入本地
                    if ('K' in vote_count) or (int(vote_count)>max_vote_count_limit):
                        answer_item_content = answer_item.find('div', class_='zm-item-rich-text')#div answer
                        answer_item_content_str = answer_item_content.text.strip()#answer文本信息
                        answer_id = answer_item['data-aid'].strip()#answer id 信息

                        #若答案的文本长度小于150，且该answer_id不包含在answer_id_set中，则为未收录answer
                        if  (answer_id not in answer_id_set) and (len(answer_item_content_str) < 150):
                            # answer_list.append(str(answer_item_content).decode('utf-8'))

                            #若为图片信息，则将 "&lt; &gt";还原为"< >"
                            if answer_item_content_str.startswith('&lt;'):
                                answer_item_content_str = answer_item_content_str.replace('&lt;', '<').replace('&gt;', '>')

                            answer_text = 'A:%s<br><div width="%s">' % (answer_item_content_str, answer_id)
                            answer_text_list.append(answer_text)

                            #该answer对应的id
                            # answer_id_obj.write(answer_id + '\n')
                            answer_id_list.append(answer_id + '\n')
                    else:
                        continue

                #若符合要求的答案不为空，则将改答案及其对应的answer_ids写入本地
                if answer_text_list:
                    Q_A_dic = {'Q':question_title, 'A':''.join(answer_text_list)}
                    json_data = json.dumps(Q_A_dic)

                    #将question,answer对应的文本信息写入到本地
                    humor_Q_A_fileObj.write(json_data + '\n')

                    #将answer对应的id写入到写入到本地
                    answer_id_obj.writelines(answer_id_list)

            except Exception, e:
                print e,url
                # print '*'*40
        humor_Q_A_fileObj.close()
        answer_id_obj.close()

    @staticmethod
    def save_Q_A():
        '''将humor_Q_A文件中问题与回答转换格式后写入本地'''
        qa_list = []
        with codecs.open('data/humor_Q_A_old_version2.txt', encoding='utf-8') as f:
            for line in f.readlines():
                json_line = json.loads(line)
                Q = BeautifulSoup(json_line['Q']).text.strip()
                A_str = BeautifulSoup(json_line['A']).text.strip()
                if A_str.startswith('&lt;'):
                    A_str = A_str.replace('&lt;', '<').replace('&gt;', '>')
                A = 'A:' + '<br>A:'.join(re.split('\n\n+', A_str))
                # print Q
                # print A
                Q_A_str = '<table><tr><td><font color="#4EABF9"><u>%s</u></font><br>%s</td></tr></table>\n' % (Q, A)
                qa_list.append(Q_A_str)

        #发送至邮箱
        # mail_to = "zhang_jie1231@163.com"
        # send_to_163_mail(''.join(qa_list), mail_to)

        #写入到本地
        codecs.open('Q_A.txt', mode='wb', encoding='utf-8').writelines(qa_list)

    @staticmethod
    def mail_Q_A(mail_to):
        '''神回复发送到邮箱中'''
        qa_list = []
        with codecs.open('humor_Q_A.txt', encoding='utf-8') as f:
            for line in f.readlines():
                json_line = json.loads(line)
                Q = json_line['Q']
                A = json_line['A']
                Q_A_str = '<div><tr><td><font color="#4EABF9"><u>%s</u></font><br>%s</td></tr></div>\n' % (Q, A)
                qa_list.append(Q_A_str)
            mail_content = ''.join(qa_list)
            send_to_163_mail(mail_content, mail_to)
    # mail_to = "sivilwang@163.com"
    # mail_Q_A(mail_to)
if __name__ == "__main__":
#     humor = HumorAnswer()
#     def get_question_ids_test():
#         start = time.time()
#         humor.get_question_ids_by_topic_id()
#         print time.time() - start
#         codecs.open('sys/questions_id_0228.txt', mode='wb', encoding='utf-8').writelines([item+'\n'for item in humor.total_question_id_set])#11343
    # get_question_ids_test()
    # def get_answer_id_test():
    #     start = time.time()
    #     humor.get_humor_answer_by_question_id()
    #     print time.time() - start
    # get_answer_id_test()
    HumorAnswer.save_Q_A()
#***********************************************************
def get_answer_id():
    '''抓取点赞数超过1000的回答的answer_id'''
    zhihu_root_url = 'http://www.zhihu.com'
    question_id_filename = os.path.join(PATH, 'question_ids.txt')
    answer_id_set = set()
    with codecs.open(question_id_filename, encoding='utf-8') as f:
        index = 0
        for line in f.readlines():
            index += 1
            question_id = line.rstrip()
            url = zhihu_root_url + question_id
            r = requests.get(url, timeout=15)
            html = r.text
            soup = BeautifulSoup(html)
            try:
                main_content = soup.find('div', class_='zu-main-content')
                answer_item_list = main_content.find_all('div', class_='zm-item-answer')
                for answer_item in answer_item_list:
                    vote_count = answer_item.find('span', class_='count').text
                    #若点赞数大于1000，则将answer_id写入本地
                    if ('K' in vote_count) or (int(vote_count)>1000):
                        answer_item_content = answer_item.find('div', class_='zm-item-rich-text')
                        data_aid = answer_item['data-aid'].strip()
                        answer_id_set.add(data_aid)
                        print index
                    else:
                        # print vote_count, data_aid
                        continue
            except:
                print url
    codecs.open('answer_ids.txt', mode='wb', encoding='utf-8').writelines([item+'\n' for item in answer_id_set])
    # get_answer_id()

#***********************************************************