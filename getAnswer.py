#coding:utf-8
__author__ = "huafeng"
import os
import re
import time
import json
import codecs
import requests
from bs4 import BeautifulSoup
PATH = os.path.dirname(os.path.abspath(__file__))

class GetAnswer(object):
    '''根据question_id文件获取answer_id，answer的内容，并写入到本地'''
    def __init__(self, question_id_filename=None, crawled_question_id_filename=None):
        if not question_id_filename:    #如果没有传入question_id_filename，则默认将./sys/all_question_id.txt作为question id 的目录
            self.question_id_filename = os.path.join(PATH, 'sys', 'all_question_id.txt')
        else:
            self.question_id_filename = question_id_filename
        if not crawled_question_id_filename:    #设置默认已抓取question_id，默认./sys/crawled_question_id.txt
            self.crawled_question_id_filename = os.path.join(PATH, 'sys', 'crawled_question_id.txt')
        else:
            self.crawled_question_id_filename = crawled_question_id_filename

        self.total_question_id_list = self._load_question_ids(self.question_id_filename) # 加载所有answer的answer_id，并去重
        self.crawled_question_id_set = set(self._load_question_ids(self.crawled_question_id_filename)) #加载所有已抓取的answer_id，并去重

    def _load_question_ids(self, filename):
        '''加载question_id信息'''
        line_list = codecs.open(filename, encoding='utf-8').readlines()
        if not line_list:
            raise ValueError('no question id in file: %s, please check' % filename)
        else:
            return [item.strip() for item in line_list]

    def get_answer_by_question_id(self, max_vote_count_limit=500, words_count=150):
        '''由question_id获取answer_id, 点赞数量限制，answer字数限制'''
        zhihu_root_url = 'http://www.zhihu.com'

        #所有answer_id的集合
        # answer_id_set = set([item.rstrip() for item in codecs.open('humor_Q_A_answer_id.txt', encoding='utf-8').readlines()])

        answer_fileObj = codecs.open(time.strftime('question_answer_content_%Y_%m_%d.txt'), mode='ab', encoding='utf-8')
        answer_id_obj = codecs.open(time.strftime('crawled_answer_id_%Y_%m_%d.txt'), mode='ab', encoding='utf-8')

        #遍历question_id，获取符合要求的answer，并将对应answer_id写入本地
        for question_id in self.total_question_id_list:
            answer_text_list = []
            answer_id_list = []
            url = zhihu_root_url + question_id
            r = requests.get(url, timeout=15)
            html = r.text
            soup = BeautifulSoup(html)
            try:
                main_content = soup.find('div', class_='zu-main-content')
                question_title = main_content.find('div', id='zh-question-title').text.strip()  #问题的标题
                answer_item_list = main_content.find_all('div', class_='zm-item-answer')    #答案列表
                for answer_item in answer_item_list:
                    vote_count = answer_item.find('span', class_='count').text.strip()
                    #若点赞数大于max_vote_count_limit，则将answer_id写入本地
                    if ('K' in vote_count) or (int(vote_count)>max_vote_count_limit):
                        answer_item_content = answer_item.find('div', class_='zm-item-rich-text')#div answer
                        answer_item_content_str = answer_item_content.text.strip()#answer文本信息
                        answer_id = answer_item['data-aid'].strip()#answer id 信息，此处解析出的20729335的标准数字格式，与answer_id

                        #若答案的文本长度小于150，且该answer_id不包含在answer_id_set中，则为未收录answer
                        if  (r'/question/'+answer_id not in self.crawled_question_id_set) and (len(answer_item_content_str) < words_count):
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
                    # Q_A_dic = {'Q':question_title, 'A':''.join(answer_text_list)}
                    # json_data = json.dumps(Q_A_dic)
                    question_title = question_title
                    answer_content = ''.join(answer_text_list)
                    Q_A_str = '<table><tr><td><font color="#4EABF9"><u>%s</u></font><br>%s</td></tr></table>\n' % (question_title, answer_content)
                    #将question,answer对应的文本信息写入到本地
                    answer_fileObj.write(Q_A_str + '\n')

                    #将answer对应的id写入到写入到本地
                    answer_id_obj.writelines(answer_id_list)

            except Exception, e:
                print e,url
                # print '*'*40
        answer_fileObj.close()
        answer_id_obj.close()


if __name__ == "__main__":
    answer = GetAnswer(question_id_filename='question_id_500.txt')
    answer.get_answer_by_question_id()

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
    # HumorAnswer.save_Q_A()