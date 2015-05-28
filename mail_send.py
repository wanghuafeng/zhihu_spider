#coding:utf-8
import smtplib
import time
from email.mime.text import MIMEText

mail_host_server = "smtp.163.com"
mail_user = 'wachfx@163.com'
mail_password = ''

def send_to_163_mail(mail_content, mailto_list):
    '''发送至邮箱'''
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    timestamp = time.strftime('%Y_%m_%d_%H%M%S')
    msg['Subject'] = 'humor ' + timestamp
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)
    s.sendmail(mail_user, mailto_list, msg.as_string())
    s.close()

def send_email_to_evernote(title, mail_content, evernote_to):
    '''发送至印象笔记'''
    evernote_note_name = u'知乎'
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    msg['Subject'] = u'%s@%s' % (title, evernote_note_name)
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.sendmail(mail_user, evernote_to, msg.as_string())
    s.connect(mail_host_server)
    s.login(mail_user, mail_password)

def send_question_content_to_email(mail_to):
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
                send_to_163_mail(''.join(mail_content_list), mail_to)
                print count
                mail_content_list =  []

if __name__ == "__main__":
    # div = '<table><tr><td><font color="#4EABF9"><u>%s</u></font><br>%s</td></tr></table>\n' %(u'王华锋', u'华锋')
    div = '<table><tr><td><font color="#4EABF9"><u>你为自己喜欢的游戏做过哪些贡献？</u></font><br>A:pay for it//算了，简短的答案最好<br><div width="11771992"></td></tr></table>'
    pic_div = '<div class="zm-item-rich-text" data-action="/answer/content" data-resourceid="3265209"><div data-original="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_r.jpg"&gt;</noscript><img class="origin_image zh-lightbox-thumb lazy" data-actualsrc="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_b.jpg" data-original="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_r.jpg" data-rawheight="760" data-rawwidth="469" src="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_b.jpg" width="469"/></div></div>'
    # div = u"<div data-editable=\"true\" id=\"zh-question-title\">\n\n<h2 class=\"zm-item-title zm-editable-content\">\n\n\u7b14\u8bb0\u672c\u7535\u8111\u6309\u4f4f\u7535\u6e90\u952e\u5f3a\u884c\u5173\u673a\uff0c\u5bf9\u7535\u8111\u6709\u4f24\u5bb3\u5417\uff1f\n\n</h2>\n</div>"
    send_to_163_mail(div, 'sivilwang@163.com')

