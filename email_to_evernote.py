#coding:utf-8
import smtplib
from email.MIMEText import MIMEText

import requests


mailto_list = "mabotree.17d688f@m.yinxiang.com"
# mailto_list = "wanghuafeng@baiwenbao.com"
mail_host_server = "smtp.qiye.163.com"
mail_user = 'wanghuafeng@baiwenbao.com'
mail_password = 'Py03thon'

def to_evernote(mail_content):
    # mail_content = ''
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    msg['Subject'] = u'页面抓取@CRF'
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)
    s.sendmail(mail_user, mailto_list, msg.as_string())
    s.close()


# url = 'http://www.cnblogs.com/xiaowuyi/archive/2012/03/17/2404015.html'
# html = requests.get(url).text
from zhitst import get_questions_by_topic_id, get_answer_by_question_id
# title, vote_count, answer = get_questions_by_topic_id()
content = get_answer_by_question_id()
to_evernote(content)
