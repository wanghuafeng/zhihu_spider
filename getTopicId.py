#coding:utf-8
import os
import re
import time
import json
import codecs
import requests
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))

class ZhihuTopicId(object):
    '''根据文件cat_id_mapping_34中的话题，解析出所有话题对应的topic_id，并写入本地。
    get_catory_id为抓取话题广场id的函数'''
    topic_root_url = 'http://www.zhihu.com/topics'#话题广场根目录
    root_url = 'http://www.zhihu.com'#根目录
    catgory_id_mapping_filename = os.path.join(PATH, 'sys', 'cat_id_mapping_34.txt')#话题广场中话题及其对应的id
    topic_id_filename = os.path.join(PATH, 'sys', time.strftime('all_topic_id_%Y_%m_%d_%H%M%S.txt'))#话题广场中对应的tipic id

    def __init__(self):
        self.chosen_id_list = []
        self._load_cat_id()
        self.cookie = self.get_cookie_param()

    def _load_cat_id(self):
        '''读取本地文件中不以#号开头的id信息，保存到self.chosen_id_list中'''
        with codecs.open(self.catgory_id_mapping_filename, encoding='utf-8') as f:
            for line in f.readlines():
                if not line.startswith('#'):
                    topic_id = line.strip().split('\t')[-1]
                    self.chosen_id_list.append(topic_id)
            print 'catagory id count:', len(self.chosen_id_list)

    def log_record(self):
        '''生成log句柄，用于记录日志'''
        log_filename = time.strftime('%Y_%m_%d.log')
        log_file = os.path.join(PATH, 'log', log_filename)
        self.log = codecs.open(log_file, mode='a', encoding='utf-8')

    @staticmethod
    def get_catory_id():
        '''解析根目录页面，获取所有话题id'''
        try:
            html = requests.get(ZhihuTopicId.topic_root_url).text
        except BaseException:
            print 'request time out...'
            try:
                html = requests.get(ZhihuTopicId.topic_root_url).text
            except BaseException:
                print 'request time out...'
                return []
        soup = BeautifulSoup(html)
        url_str = soup.find('ul', class_="zm-topic-cat-main clearfix")
        url_li_list = url_str.find_all('li', attrs={'data-id':True})
        catagory_id_list = [(item.a.text, item['data-id']) for item in url_li_list]
        print catagory_id_list
        return catagory_id_list
        # codecs.open('cat_id_mapping.txt', mode='wb', encoding='utf-8').writelines([('\t'.join(item) + '\n') for item in url_list])

    def get_cookie_param(self):
        '''获取cookie信息'''
        cookie = requests.get(self.topic_root_url).cookies.get('_xsrf')
        print 'cookie info: ', cookie
        return cookie

    def get_topic_id_by_catarory_id(self, cattopic_id):
        '''由cattopic_id获取topic_id，这里去zhihu默认的请求次数（3次），即每个cattopic_id对应60个topic_id(/topic/19553298)'''
        topic_url = 'http://www.zhihu.com/node/TopicsPlazzaListV2'
        total_topic_id_set = set()
        for offset_index in range(3):
            post_data = {
                'method':'next',
                'params':'{"topic_id":%s,"offset":%d,"hash_id":""}',
                '_xsrf':self.cookie,
                }
            post_data['params'] = post_data['params'] % (cattopic_id, offset_index*20)
            json_html = requests.post(topic_url, data=post_data).text
            json_data = json.loads(json_html)
            msg_list = json_data.get('msg')
            topic_url_list = [BeautifulSoup(item).find('a')['href'] for item in msg_list]
            total_topic_id_set |= set(topic_url_list)
        print 'total topic count:', len(total_topic_id_set)
        return total_topic_id_set

    def write_all_topic_id(self):
        total_id_set = set()
        for cattopic_id in self.chosen_id_list:
            total_id_set |= self.get_topic_id_by_catarory_id(cattopic_id)
        print 'topic id count:', len(total_id_set)#1524据个人习惯过滤后，余22个标签的1014个topic_id
        codecs.open(self.topic_id_filename, mode='wb', encoding='utf-8').writelines([item+'\n' for item in total_id_set])

if __name__ == "__main__":
    def write_all_topic_id():
        zhihu = ZhihuTopicId()
        start_time = time.time()
        zhihu.write_all_topic_id()
        print time.time() - start_time
    # write_all_topic_id()

    def utils_test():
        zhihu = ZhihuTopicId()
        zhihu.get_catory_id()
        zhihu.get_cookie_param()
        zhihu.get_topic_id_by_catarory_id('1027')

    def gen_all_topic_url_list():
        ZhihuTopicId.get_catory_id()
    # gen_all_topic_url_list()