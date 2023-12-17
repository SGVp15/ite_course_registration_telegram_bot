import base64
import imghdr
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

environment = Environment(auto_reload=True, loader=FileSystemLoader('./Config/template_email'))
chillde_present = environment.get_template('chillde_present.html')


def send_c(send_to='g.savushkin@itexpert.ru', file='1500_1099737895172.pdf'):
    sender_email = 'life@itexpert.ru'
    password = 'f4MSl5iw60codB'

    text = '''Друзья, перед новым годом мы все становимся чуть романтичнее, возвращаемся в детство, стремимся порадовать детей и создать для них особую атмосферу праздника 🎄✨
    IT Expert, как всегда, уделяет особое внимание детям нашей команды 👶
    Пускай у наших детей будут неограниченные возможности и все необходимое для счастливой и полноценной жизни рядом со спокойными родителями, уверенными в завтрашнем дне. Мы знаем – каждый член нашей команды делает все возможное для уверенного завтрашнего дня 🌟
    В качестве подарка мы выбрали сертификаты Ozon, на маркетплейсе которого можно выбрать все, что порадует детей с первых дней рождения вплоть до совершеннолетия. Сертификаты находятся во вложении к этому письму. Обратите внимание, что срок активации сертификатов до 16.12.2023 г., важно использовать их до окончания этого срока.
    Теплых вам праздничных дней рядом с семьей 🎄'''

    msg = EmailMessage()
    msg['Subject'] = "Новогодние_подарки_для_детей 🎁🎄"
    msg['From'] = sender_email
    msg['To'] = send_to

    with open('./images/image.png', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename='card.png')

    with open(f'./ozon/{file}', 'rb') as f:
        file_data = f.read()
        file_name = f.name
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='ozon_certificate.pdf')

    path = './images/image.png'
    with open(path, mode='rb') as f:
        s = f.read()
    base64_file = base64.b64encode(s)
    base64_file = base64_file.decode("utf-8")

    html = chillde_present.render()

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(host='smtp.yandex.ru', port=465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)
