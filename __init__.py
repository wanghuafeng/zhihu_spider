__author__ = 'wanghuafeng'
#coding:utf-8
import os
import re
import time
import codecs
import requests
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))

class ZhiHu(object):
    topic_root_url = 'http://www.zhihu.com/topics'#话题广场根目录
    def __init__(self):
        self.log_record()
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
        url_list = url_str.find_all('li', attrs={'data-id':True})
        print url_list
if __name__ == "__main__":
    zhihu = ZhiHu()
    start_time = time.time()
    zhihu.gen_all_topic_url_list()
    print time.time()-start_time