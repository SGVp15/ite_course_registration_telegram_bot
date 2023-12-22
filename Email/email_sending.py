import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from Config.config import SMTP_SERVER, SMTP_PORT
from Config.config_private import EMAIL_LOGIN, EMAIL_PASSWORD, email_login_password
import os


class EmailSending:
    def __init__(self, subject='Вы зарегистрированы на курс', from_email=EMAIL_LOGIN, to='', cc='', bcc='',
                 text='', html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
                 user=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None, files_path=[]):
        """

        :type text: Plain text Email, if html not support
        """
        self.subject = subject
        self.from_email = from_email
        self.to_addrs = []
        self.to = to
        self.cc = cc
        self.bcc = bcc
        for x in [self.to, self.cc, self.bcc]:
            if type(x) is list:
                self.to_addrs.extend(x)
            elif x != '':
                self.to_addrs.append(x)

        self.text = text
        self.html = html
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        if manager:
            try:
                self.password = email_login_password[manager]
                self.user = manager
                self.from_email = manager
            except KeyError:
                pass
        self.files = files_path

    def send_email(self):
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['Subject'] = self.subject
            msg['To'] = self.to
            msg['Cc'] = self.cc
            msg['Bcc'] = self.bcc

            part1 = MIMEText(self.text, 'plain')
            part2 = MIMEText(self.html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            # for file in self.files:
            #     with open(file, 'rb') as f:
            #         file_data = f.read()
            #         file_name = os.path.basename(file)
            #         msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            for file in self.files:
                with open(file, "rb") as f:
                    file_name = os.path.basename(file)
                    part = MIMEApplication(f.read(), file_name=file_name)
                # After the file is closed
                part['Content-Disposition'] = f'attachment; filename={file_name}'
                msg.attach(part)

            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            smtp.login(self.user, self.password)
            smtp.sendmail(from_addr=self.from_email, to_addrs=self.to_addrs, msg=msg.as_string())
            smtp.quit()

            return f'Email send {self.to_addrs}'

        except Exception as e:
            return f'Error {e}'
