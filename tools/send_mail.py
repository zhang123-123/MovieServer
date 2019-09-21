# -*- coding: utf-8 -*-
def send_email(subject, content, filepath, receive_email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    sender = 'zhang864071694@163.com'  # 发送方邮箱
    passwd = 'zhangzenan520'  # 填入发送方邮箱的授权码
    receivers = receive_email  # 收件人邮箱
    msgRoot = MIMEMultipart()
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    if len(receivers) > 1:
        msgRoot['To'] = ','.join(receivers)  # 群发邮件
    else:
        msgRoot['To'] = receivers[0]
    part = MIMEText(content, _charset="utf-8")
    msgRoot.attach(part)
    for path in filepath:
        part = MIMEApplication(open(path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=path)
        msgRoot.attach(part)
    s = smtplib.SMTP('smtp.163.com', 25)
    try:
        s.login(sender, passwd)
        s.sendmail(sender, receivers, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error, 发送失败")
    finally:
        s.quit()


if __name__ == '__main__':
    subject = "邮件标题"
    content = "Python 邮件正文"
    receive_email = ["864071694@qq.com", "zhang864071694@163.com"]
    send_email(subject, content, ["config.py"], receive_email)
