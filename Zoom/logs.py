from datetime import datetime

from Config.config import LOG_BACKUP, LOG_FILE
from Zoom.sort_csv import remove_sort_csv


def log_write(user, url: str, course: str, file_logs=LOG_FILE, status: str = 'ERROR', sep=','):
    log = {'time': datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
           'status': status,
           'course': course,
           'last_name': user.last_name,
           'fist_name': user.first_name,
           'email': user.email}

    if url:
        log[url] = url
    else:
        log[status] = '[ERROR]'

    with open(file_logs, mode='a', encoding='utf-8') as f:
        logs = sep.join(list(log.values()))
        f.write(logs + '\n')


def backup_log(file=LOG_FILE, file_backup=LOG_BACKUP):
    with open(file, mode='r', encoding='utf-8') as f:
        s = f.read()
    with open(file_backup, mode='a', encoding='utf-8') as f:
        f.write(s)
    remove_sort_csv(file=file_backup)

