import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Config.config import EMAILS_SALLER, SMTP_SERVER, PORT_SMTP
from Config.config_private import EMAIL_LOGIN, EMAIL_PASSWORD


class EmailSending:
    def __init__(self, subject='Вы зарегистрированы на курс', from_email=EMAIL_LOGIN, to='', cc='', bcc=EMAILS_SALLER,
                 text='PlainText', html=''):
        self.subject = subject
        self.from_email = from_email

        if type(to) == list:
            self.to = ';'.join(to)
        else:
            self.to = to
        self.to = to

        if type(cc) == list:
            self.cc = ';'.join(cc)
        else:
            self.cc = cc

        if type(bcc) == list:
            self.bcc = ';'.join(bcc)
        else:
            self.bcc = bcc

        self.text = text
        self.html = html

    def send_email(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_LOGIN
        msg['Subject'] = self.subject
        msg['To'] = self.to
        msg['Bcc'] = self.bcc
        msg['Cc'] = self.cc

        part1 = MIMEText(self.text, 'plain')
        part2 = MIMEText(self.html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        smtp = smtplib.SMTP_SSL(SMTP_SERVER, PORT_SMTP)
        smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.sendmail(from_addr=self.from_email, to_addrs=self.to, msg=msg.as_string())
        smtp.quit()
        print('Email send', self.to)
