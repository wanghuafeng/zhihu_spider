#coding:utf-8
import smtplib
from email.mime.text import MIMEText

import requests


mailto_list = "mabotree.17d688f@m.yinxiang.com"
mail_host_server = "smtp.qiye.163.com"
mail_user = 'wanghuafeng@baiwenbao.com'
mail_password = 'Py03thon'

def send(mail_content):
    # mail_content = ''
    msg = MIMEText(mail_content, _subtype='html', _charset='gbk')
    msg['Subject'] = u'页面抓取@语言学系'
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)
    s.sendmail(mail_user, mailto_list, msg.as_string())
    s.close()


url = 'http://www.cnblogs.com/xiaowuyi/archive/2012/03/17/2404015.html'
html = requests.get(url).text

# send(html)