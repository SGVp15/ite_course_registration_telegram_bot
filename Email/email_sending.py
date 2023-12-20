from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from Config.config import EMAILS_SALLER, SMTP_SERVER, PORT_SMTP
from Config.config_private import EMAIL_LOGIN, EMAIL_PASSWORD
import smtplib


class EmailSending:
    def __init__(self, subject='', from_email=EMAIL_LOGIN, to='', bcc=EMAILS_SALLER, text=''):
        self.subject = subject
        self.from_email = from_email
        self.to = to
        self.bcc = bcc
        self.text = text

    def send_email(self):
        strFrom = self.from_email
        strTo = self.to
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = strFrom
        msgRoot['lllllllll'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText(text, 'html')
        msgAlternative.attach(msgText)

        # This example assumes the image is in the current directory
        # fp = open('test.jpg', 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()

        # Define the image's ID as referenced above
        # msgImage.add_header('Content-ID', '<image1>')
        # msgRoot.attach(msgImage)

        # Send the email (this example assumes SMTP authentication is required)

        smtp = smtplib.SMTP()
        smtp.connect(SMTP_SERVER, port=PORT_SMTP)
        smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.sendmail(strFrom, strTo, msgRoot.as_string())
        smtp.quit()
