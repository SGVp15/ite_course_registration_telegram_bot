import random
import re
import time

import pyperclip


def generator_password():
    random.sample()


def replace_string(s: str) -> str:
    rows = s.split('\n')
    out = []
    for row in rows:
        row = row.strip()
        try:
            email = re.findall(r'(\S*@\S*)', row)[0]
            row = re.sub(r'(\S*@\S*)', '', row)

            row = row.split(' ')
            first_name = row[1]
            last_name = row[0]
            out.append(f'{first_name}\t{last_name}\t\t\t\t{email}')
        except Exception:
            pass
    s = '\n'.join(out)
    return s


if __name__ == '__main__':
    while True:
        clipboard = pyperclip.paste()
        if len(re.findall(r'\t{2}', clipboard)) == 0:
            pyperclip.copy(replace_string(clipboard))
        time.sleep(0.1)
