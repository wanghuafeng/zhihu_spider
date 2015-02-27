#coding:utf-8
import smtplib
import time
from email.MIMEText import MIMEText



# mailto_list = "mabotree.17d688f@m.yinxiang.com"
# mailto_list = 'wanghuafengc.4742cf0@m.yinxiang.com '
# mailto_list = "wanghuali225.972fe30@m.yinxiang.com"
# mailto_list = "mabotree.17d688f@m.yinxiang.com"
mailto_list = "sivilwang@163.com"
mail_host_server = "smtp.qiye.163.com"
mail_user = 'wanghuafeng@baiwenbao.com'
mail_password = 'Py03thon'

def send_to_163_mail(mail_content):
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    timestamp = time.strftime('%Y_%m_%d_%H%M%S')
    msg['Subject'] = timestamp
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)
    s.sendmail(mail_user, mailto_list, msg.as_string())
    s.close()

def send_email_to_evernote(title, mail_content):
    evernote_note_name = u'知乎'
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    msg['Subject'] = u'%s@%s' % (title, evernote_note_name)
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.sendmail(mail_user, mailto_list, msg.as_string())
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)

def send_question_content_to_email():
    import os
    import json
    import codecs
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
                to_evernote(''.join(mail_content_list))
                print count
                mail_content_list =  []

if __name__ == "__main__":
    from zhihu import  get_answer_by_question_id
    url = 'http://www.zhihu.com/question/19568396'
    title, content = get_answer_by_question_id(url)
    to_evernote(title,content)


# to_evernote('zhihu')
# if __name__ == "__main__":
#     # url = 'http://www.cnblogs.com/xiaowuyi/archive/2012/03/17/2404015.html'
#     # html = requests.get(url).text
#     from zhitst import get_questions_by_topic_id, get_answer_by_question_id
#     # title, vote_count, answer = get_questions_by_topic_id()
#     content = get_answer_by_question_id()
#     to_evernote(content)