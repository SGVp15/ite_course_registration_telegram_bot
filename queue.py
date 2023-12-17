import os

from Contact.Contact import User
from Contact.parser import get_users_from_string
from Config.config import QUEUE, OLD_USERS

# class Queue:
#@staticmethod
def delete_duplicates_in_queue_file(file=QUEUE):
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    rows = s.split('\n')
    end_rows = []
    for row in rows:
        if row not in end_rows and row != '':
            end_rows.append(row)
    with open(file=file, mode='w', encoding='utf-8') as f:
        f.write('\n'.join(end_rows) + '\n')

#@staticmethod
def del_user_from_temp_file(file=QUEUE):
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    s = s.split('\n')
    s = '\n'.join(s[1:])
    with open(file=file, mode='w', encoding='utf-8') as f:
        f.write(s)

#@staticmethod
def add_to_queue_file(user: User, file: str = QUEUE):
    with open(file=file, mode='a', encoding='utf-8') as f:
        f.write(str(user) + '\n')
    delete_duplicates_in_queue_file()

#@staticmethod
def get_user_from_queue_file(file=QUEUE) -> User:
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    rows = s.split('\n')
    users = []
    for row in rows:
        if row:
            l = row.split('\t')
            last_name = l[0]
            first_name = l[1]
            email = l[2]
            url_registration = l[3]
            course = l[4]
            users.append(
                User(last_name=last_name, first_name=first_name, email=email, url_registration=url_registration,
                     course=course))

    # users = get_users_from_string(s)
    if users:
        return users[0]

#@staticmethod
def clear_queue(file=QUEUE):
    with open(file, mode='w', encoding='utf-8') as file:
        file.write('')

#@staticmethod
def get_queue(file_path=QUEUE):
    with open(file_path, mode='r', encoding='utf-8') as file_path:
        queue = file_path.read()
        if queue == '':
            return 'Очередь пустая!\n'
        else:
            return queue

#@staticmethod
def get_old_users() -> list[User]:
    if os.path.exists(OLD_USERS):
        old_users = []
        with open(OLD_USERS, encoding='utf-8', mode='r') as file:
            rows = file.read()
            for row in rows.split('\n'):
                try:
                    old_users.extend(get_users_from_string(row))
                except Exception as e:
                    print(e)
        return old_users

#@staticmethod
def add_new_users_to_queue(input_string: str) -> list[User]:
    old_users = get_old_users()
    input_users = get_users_from_string(input_string)
    users = [user for user in input_users if user not in old_users]
    for user in users:
        add_to_queue_file(user)
    return users
