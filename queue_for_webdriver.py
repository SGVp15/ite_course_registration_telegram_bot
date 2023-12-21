import os

from Config.config import QUEUE, OLD_USERS
from Contact.Contact import User
from Contact.parser import get_users_from_event_row


# class Queue:
# @staticmethod
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


# @staticmethod
def del_user_from_temp_file(file=QUEUE):
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    s = s.split('\n')
    s = '\n'.join(s[1:])
    with open(file=file, mode='w', encoding='utf-8') as f:
        f.write(s)


# @staticmethod
def add_to_queue_file(users: list[User], file: str = QUEUE):
    with open(file=file, mode='a', encoding='utf-8') as f:
        for user in users:
            f.write(str(user) + '\n')
    delete_duplicates_in_queue_file()


# @staticmethod
def get_users_from_queue_file(file=QUEUE) -> list[User]:
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    return get_users_from_event_row(s)


# @staticmethod
def clear_queue(file=QUEUE):
    with open(file, mode='w', encoding='utf-8') as file:
        file.write('')


# @staticmethod
def get_queue(file_path=QUEUE) -> str:
    with open(file_path, mode='r', encoding='utf-8') as file_path:
        s = file_path.read().strip()
        if s == '':
            return 'Очередь пустая!\n'
        else:
            return s


# @staticmethod
def get_old_users() -> list[User]:
    if os.path.exists(OLD_USERS):
        with open(OLD_USERS, encoding='utf-8', mode='r') as file:
            s = file.read()
        return get_users_from_event_row(s)
