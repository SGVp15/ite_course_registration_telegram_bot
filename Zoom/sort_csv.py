import re

from Config.config import LOG_FILE


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
    except ValueError:
        pass
    if sort:
        sorted(rows, reverse=True)
    s = '\n'.join(rows)
    s = s.strip()

    with open(file=file, mode='w', encoding='utf-8') as f:
        f.write(s + '\n')
