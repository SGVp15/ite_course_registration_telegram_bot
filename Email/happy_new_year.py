import os
from copy import copy

from Email import EmailSending


class UserTEMP:
    def __init__(self, name, email, num_chiled, files=[]):
        self.name = name
        self.email = email
        self.files = files
        self.num_chiled = int(str(num_chiled).strip())


class TestEmailSending:
    def get_users(self) -> [UserTEMP]:
        users = []
        pdf_dir = 'data/happy_new_year/pdf-zip/'

        files = os.listdir(pdf_dir)
        with open('./data/happy_new_year/user.txt', mode='r', encoding='utf-8') as f:
            s = f.read()
            rows = s.split('\n')
            for row in rows:
                _list = row.split('\t')
                if _list:
                    users.append(UserTEMP(*_list))

        for u in users:
            _files = []
            for _ in range(u.num_chiled):
                file = files.pop()
                _files.append(os.path.join(pdf_dir, file))
            u.files = copy(_files)
        return users

    def send_email(self):
        subject = 'Новогодние подарки для детей 🎁🎄'

        with open('./Email/template_email/child_present.html', mode='r', encoding='utf-8') as f:
            html = f.read()

        with open('./data/happy_new_year/log.txt', mode='a', encoding='utf-8') as f:
            for user in self.get_users():
                email = EmailSending(from_email='life@itexpert.ru',
                                     login='life@itexpert.ru',
                                     subject=subject,
                                     to=user.email,
                                     files_path=user.files,
                                     html=html).send_email()
                f.write(f'{user} [ok]\n')


TestEmailSending().send_email()
