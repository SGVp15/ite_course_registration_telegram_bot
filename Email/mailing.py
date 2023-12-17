import time

from Contact import parser
from Email.send_email import send_email_url_connection


def send_all_from_logs(file='./data/.log.txt'):
    with open(file, mode='r', encoding='utf-8') as f:
        s = f.read()
    rows = s.split('\n')
    users = []
    for row in rows:
        users.extend(parser.get_users_from_string(row))

    for user in users:
        print(f'{user.last_name}\t\t{user.url_registration}')
        send_email_url_connection(user)
        time.sleep(1)
