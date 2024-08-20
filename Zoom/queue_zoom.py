import os
import pickle

from Config.config import QUEUE, OLD_USERS
from Contact import Contact


class Queue:
    def __init__(self, file=QUEUE):
        self.file = file
        self.users: [Contact] = []
        self.load_queue()

    def save_queue(self):
        self.del_duplicates_users()
        pickle.dump(self.users, open(file=self.file, mode='wb'))

    def load_queue(self):
        if os.path.exists(self.file):
            self.users: [Contact] = pickle.load(open(file=self.file, mode='rb'))

    def add_users(self, new_users: [Contact]):
        self.users.extend(new_users)
        self.save_queue()

    def del_duplicates_users(self):
        users = []
        for user in self.users:
            if user not in users:
                users.append(user)
        self.users = users

    def del_user(self, user):
        self.users.remove(user)
        self.save_queue()


def clear_queue():
    if os.path.exists(QUEUE):
        os.remove(QUEUE)


def get_queue(file_path=QUEUE) -> [Contact]:
    if os.path.exists(file_path):
        return pickle.load(open(file=file_path, mode='rb'))
    return []


def load_old_users() -> [Contact]:
    if os.path.exists(OLD_USERS):
        return pickle.load(open(file=OLD_USERS, mode='rb'))
    return []


def save_old_users(user):
    users = load_old_users()
    users.append(user)
    pickle.dump(users, open(file=OLD_USERS, mode='wb'))
