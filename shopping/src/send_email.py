# -*- encoding:utf8 -*-

import smtplib
from email.mime.text import MIMEText

msg_from = '************@qq.com'   # 发送方邮箱
passwd = '*************'     # 填入发送方邮箱的授权码
subject = "邮件验证"            # 主题


# msg_to是收件人邮箱，content是发送的内容
def send(content="000000",msg_to='*********@qq.com'):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)   # 邮件服务器及端口号
        s.login(msg_from, passwd)                   #登录邮箱
        s.sendmail(msg_from, msg_to, msg.as_string())
        print "发送成功"
    except s.SMTPException, e:
        print "发送失败"
    finally:
        s.quit()

# send("798654","2801293031@qq.com")
