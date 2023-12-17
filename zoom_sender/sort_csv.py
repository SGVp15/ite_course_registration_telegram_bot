import re

from Config.config import LOG_BACKUP
from Config.config import LOG_FILE

LOG_BACKUP
LOG_FILE


def remove_sort_csv(file=LOG_FILE, sort=True):
    with open(file=file, mode='r', encoding='utf-8') as f:
        s = f.read()
    s = s.strip()
    # s = re.sub(r'\[OK]', r'\n[OK]', s)
    s = re.sub(r', {2,}', ', ', s)
    rows = s.split('\n')
    rows = set(rows)
    rows = list(rows)
    try:
        rows.remove('')
    except:
        pass
    if sort:
        rows.sort(reverse=True)
    s = '\n'.join(rows)
    s = s.strip()

    with open(file=file, mode='w', encoding='utf-8') as f:
        f.write(s + '\n')


if __name__ == '__main__':
    remove_sort_csv(LOG_BACKUP)
    pass
