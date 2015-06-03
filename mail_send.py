#coding:utf-8
import smtplib
import os
import time
from email.mime.text import MIMEText

PATH = os.path.dirname(os.path.abspath(__file__))

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

if __name__ == "__main__":
    mail_to = 'zhihuspider@163.com'
    def send_div_content():
        # div = '<table><tr><td><font color="#4EABF9"><u>%s</u></font><br>%s</td></tr></table>\n' %(u'王华锋', u'华锋')
        div = '<table><tr><td><font color="#4EABF9"><u>你为自己喜欢的游戏做过哪些贡献？</u></font><br>A:pay for it//算了，简短的答案最好<br><div width="11771992"></td></tr></table>'
        pic_div = '<div class="zm-item-rich-text" data-action="/answer/content" data-resourceid="3265209"><div data-original="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_r.jpg"&gt;</noscript><img class="origin_image zh-lightbox-thumb lazy" data-actualsrc="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_b.jpg" data-original="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_r.jpg" data-rawheight="760" data-rawwidth="469" src="http://pic3.zhimg.com/ea406d2b3978683c3af4c306dca85bee_b.jpg" width="469"/></div></div>'
        # div = u"<div data-editable=\"true\" id=\"zh-question-title\">\n\n<h2 class=\"zm-item-title zm-editable-content\">\n\n\u7b14\u8bb0\u672c\u7535\u8111\u6309\u4f4f\u7535\u6e90\u952e\u5f3a\u884c\u5173\u673a\uff0c\u5bf9\u7535\u8111\u6709\u4f24\u5bb3\u5417\uff1f\n\n</h2>\n</div>"
        div = '<table><tr><td><font color="#4EABF9"><u>高考为什么迟到十七分钟就不让人进了？</u></font><br>A:为什么人们总是一边想着法外开恩，一边抱怨社会不公呢？<br><div width="2108939"></td></tr></table>'
        send_to_163_mail(div, mail_to)
    # send_div_content()
    def send_file_content():
        import re
        import codecs
        import time
        file_pattern = r'E:\github\zhihu_spider\data\question_answer_content_2015_05_24.txt.partial_%s'
        # filename = os.path.join(PATH, 'data', 'question_answer_content_2015_05_24.txt.partial_10.html')
        # filename = r'E:\github\zhihu\text_data\zhihu_v500_l0-100_d20150228_r1272-1910.html'
        # file_content = codecs.open(filename).read()
        for file_index in range(1, 11):
            filename = file_pattern % file_index
            print file_index
            new_line_list = []
            with codecs.open(filename, encoding='utf-8') as f:
                index = 0
                for line in  f.readlines():
                    line = re.sub(r'\<div width="\d+"\>', '', line)
                    question_subject_match = re.search(r'<table><tr><td><font color="#4EABF9"><u>(.*?)</u></font>', line)
                    answer_list = re.findall(r'A:.*?<br>', line)
                    if (not question_subject_match):
                        print line.strip()
                        continue

                    for answer in answer_list:
                        if not answer.replace('A:', '').strip():
                            print line.strip()
                            continue
                    index += 1
                    new_line = question_subject_match.group().strip().replace('<u>', '<u>%s' % index) + "\n<br>" + "\n".join(answer_list)+'</tr></td></table>'#网页显示，不需要考虑\n的问题
                    new_line_list.append(new_line)

            file_content = '\n'.join(new_line_list)
            send_to_163_mail(file_content, mail_to)
            time.sleep(3)
            codecs.open(filename + '.html', mode='wb', encoding='utf-8').write('<html><head><meta charset=\'utf-8\'></head><body>'+'\n'.join(new_line_list)+'</body></html>')
    # send_file_content()

