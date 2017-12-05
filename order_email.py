import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import settings

#Send email exposure to client script
def sendemail(df):
    from_addr = settings.from_addr
    to_addr_list = settings.to_addr_list
    subject = settings.subject
    email_template = open(settings.email_template,'r').read()
    email_content = email_template.format(df=df.to_html())

    login = settings.login
    password = settings.password
    smtpserver = settings.smtpserver

    if settings.simulate:
        print(email_content)
    else:
        send(from_addr, to_addr_list, subject, email_content, login, password, smtpserver)

#Send email server communication handling
def send(from_addr, to_addr_list, subject, email_content, login, password, smtpserver):
    fromaddr = from_addr
    toaddr = ','.join(to_addr_list)

    message = MIMEMultipart()
    message['From'] = fromaddr
    message['To'] = toaddr
    message['Subject'] = subject

    email_body = MIMEText(email_content, 'html')
    message.attach(email_body)
    msg_full = message.as_string()

    server = smtplib.SMTP(smtpserver)
    server.ehlo()
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, msg_full)
    server.quit()
