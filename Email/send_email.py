import base64
import imghdr
import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from Config import EMAIL_LOGIN, EMAIL_PASSWORD


def send_email_with_attachment(send_to: list, text='', file: str = './data/.log.txt'):
    msg = EmailMessage()
    msg['From'] = EMAIL_LOGIN
    msg['Subject'] = 'Zoom registration'
    msg['To'] = ', '.join(send_to)

    msg.set_content(text)
    if file != '':
        msg.add_attachment(open(file, 'r', encoding='utf-8').read(), filename='log.txt')

    smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
    print('Письмо отправил')


def send_email_childe_congratulation(send_to: str, file: str = ''):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_LOGIN
    msg['Subject'] = 'Zoom registration'
    msg['To'] = send_to

    path = './images/image.png'
    with open(path, mode='rb') as f:
        s = f.read()
    base64_file = base64.b64encode(s)
    base64_file = base64_file.decode("utf-8")

    with open(path, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    part = MIMEBase('application', "octet-stream")
    with open('./ozon/' + file, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename=attachment.pdf'.format(Path(path).name))
    msg.attach(part)

    smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()


def send_email_url_connection(user: Contact):
    msg = EmailMessage()
    msg['From'] = EMAIL_LOGIN
    msg['Subject'] = 'Zoom registration'
    msg['To'] = user.email
    # msg['Bcc'] = 'g.savushkin@itexpert.ru'
    msg.set_content(f'Добрый день, {user.last_name} {user.first_name}.\n'
                    # f'Завтра для подключения просьба использовать ссылку, которая отправлена Вам сегодня после 15:00.\n'
                    f'Высылаем Вам правильную ссылку на обучение:\n\n'
                    f'{user.url_registration}\n\n'
                    f'Желаем Вам приятного обучения.\n\n'
                    f'С уважением, IT Expert.')

    smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()


# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


# Define these once; use them twice!
def test_email():
    strFrom = 'from@example.com'
    strTo = 'to@example.com'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'test message'
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
    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('test.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)
    import smtplib
    smtp = smtplib.SMTP()
    smtp.connect('smtp.example.com')
    smtp.login('exampleuser', 'examplepass')
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
