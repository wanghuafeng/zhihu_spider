#coding:utf-8
__author__ = "huafeng"
import re
import os
import codecs
import requests
from bs4 import BeautifulSoup
PATH = os.path.dirname(os.path.abspath(__file__))

class QuestionId(object):
    '''遍历传入的topic_id，获取对应id下的所有的answer_id'''
    def __init__(self, topic_id_filename=None, question_id_filename=None):
        ''''''
        if not topic_id_filename:#如果没有传入topic_id_filename，则默认将./sys/all_topic_id.txt作为topic id 的目录
            self.topic_id_filename = os.path.join(PATH, 'sys', 'all_topic_id.txt')
        else:
            self.topic_id_filename = topic_id_filename
        if not question_id_filename:#如果没有传入question_id_filename，则默认将./sys/all_question_id.txt作为question id 的目录
            self.question_id_filename = os.path.join(PATH, 'sys', 'all_question_id.txt')
        else:
            self.question_id_filename = question_id_filename
        self.total_topic_list = self._load_topic_ids()  #加载topic id 文件

    def _load_topic_ids(self):
        '''读取所有的topic_id信息，由分析，知乎topic_id共1524个，这个数字至少在6个月内没有发生改变，所以此处暂且认为此值是不变的'''
        topic_list = codecs.open(self.topic_id_filename, encoding='utf-8').readlines()
        if not topic_list:
            raise ValueError('no topic id in file: %s, please check' % self.topic_id_filename)
        else:
            return [item.strip() for item in topic_list]

    def get_question_list_by_topic_id(self, topic_id, vote_count):
        '''根据topic_id解析出所有的question_id,并返回'''
        topic_url_pattern = 'http://www.zhihu.com{}/top-answers?page=%s'.format(topic_id.rstrip())
        total_question_id_list = []
        for page_index in range(1, 51):#对于每一个topic_id,top-answer最多返回50页
            page_question_id_list = []
            topic_url = topic_url_pattern % page_index
            try:
                r = requests.get(topic_url, timeout=15)
            except:
                print "timeout url:", topic_url
                continue
            if r.status_code == 404:
                continue
            html = r.text
            soup = BeautifulSoup(html)
            try:
                div_level_list = soup.find_all('div', class_='content') #该topic下的所有问题
                for question_div in div_level_list:
                    #该topic下第一个问题的相关信息
                    question_id = question_div.h2.a['href']

                    answer_vote_count = question_div.find('a', class_='zm-item-vote-count').text.strip()
                    if ('K' in answer_vote_count) or (int(answer_vote_count) > vote_count):
                        # print answer_id, answer_vote_count
                        # question_list.append(question_id)
                        page_question_id_list.append(question_id.strip())

                total_question_id_list.extend(page_question_id_list)
            except BaseException, e:
                print e, topic_url
                continue
            if not page_question_id_list:
                #若返回question_list为空，则停止翻页
                return total_question_id_list
        return total_question_id_list

    def get_all_question_id(self, vote_count):
        '''读取本地文件中的topic_id并解析所有question_id，写入到本地'''
        total_id_list_len = len(self.total_topic_list)
        all_question_id_list = []
        all_question_id_set = set()
        topic_index = 0
        for topic_id in self.total_topic_list:
            topic_index += 1
            print total_id_list_len, topic_index, #topic_id 总数，当前序列号
            topic_question_list = self.get_question_list_by_topic_id(topic_id, vote_count)#读取一个topic_id，返回所有的answer_id。
            print len(topic_question_list)#该topic_id对应的answer_id的个数
            # all_question_id_list.extend(topic_question_list)
            all_question_id_set |= set(topic_question_list)
            codecs.open(self.question_id_filename, mode='ab', encoding='utf-8').writelines([item+'\n' for item in all_question_id_set])

if __name__ == "__main__":
    #控制台打印数据，第一列为topic_id书，第二列为当前topic_id序列号，第三列为该topic对应的answer个数
    vote_count = 500    #
    question_id_filename = os.path.join(PATH, 'sys', 'question_id_%s.txt'%vote_count)
    qi = QuestionId(question_id_filename=question_id_filename)
    qi.get_all_question_id(vote_count)