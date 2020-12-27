#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mailTo(Objs, title, content, format="plain"):
    my_sender ='861759757@qq.com'    # 发件人邮箱账号
    my_pass = 'cszuniqspikcbeeg'     # 发件人邮箱密码
    ret=True
    try:
        msg=MIMEText(content,format,'utf-8')
        msg['From']=formataddr(["自动提醒",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["FK",Objs[0]])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']=title                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, Objs, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret


if __name__ == "__main__":
    sender_to = ['861759757@qq.com', ]      # 收件人邮箱账号，我这边发送给自己
    #  "thl4z6d@163.com"
    ret=mailTo(sender_to, "测试", "这是一次测试")
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
