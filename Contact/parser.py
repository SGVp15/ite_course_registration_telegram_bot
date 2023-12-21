import datetime
import re

from Config.config import PATTERN_REGISTRATION_URL, PATTERN_WEBINAR_SESSION_ID
from Contact import User


def parsing_cyrillic(row) -> list:
    row = re.sub(r'[^ А-Яа-яЁё]+', '', row)
    cyrillic = re.findall(r'([А-Яа-яЁё]+)', row)
    return cyrillic


def get_users_from_string(s: str) -> list[User]:
    s = refactor_string(s)
    couse_name, date,  teacher, course = get_course_info_from_string(s)
    url = parsing_for_pattern(row=s, pattern=fr'\s*({PATTERN_REGISTRATION_URL})\s*')

    webinar_eventsid = parsing_for_pattern(row=s, pattern=fr'\s*{PATTERN_WEBINAR_SESSION_ID}\s*')
    if webinar_eventsid == '':
        webinar_eventsid = parsing_for_pattern(row=s, pattern=fr'''\s*self.webinar_eventsid='(\w+)'\s*''')

    rows = s.split('\n')

    users = []
    for row in rows:
        emails = re.findall(r'(\S*@\S*)', row)
        row = re.sub(r'(\S*@\S*)', '', row)
        if not emails:
            continue
        curator_email = ''
        if len(emails) > 1:
            curator_email = emails[1]
        email = emails[0]
        email = re.sub(r'[^@\w_\-.]', '', email.lower())

        row = re.sub(r'(\S*@\S*)', '', row)
        row = re.sub(r'[^A-Za-z А-Яа-яЁё]+', '', row)
        name = parsing_cyrillic(row)
        try:
            user = User(last_name=name[0], first_name=name[1], email=email, url_registration=url, course=course,
                        webinar_eventsid=webinar_eventsid, curator_email=curator_email, webinar_name=couse_name,
                        date=date, teacher=teacher)
            users.append(user)
        except IndexError:
            pass
    return users


def parsing_for_pattern(row: str, pattern: str) -> str:
    s = refactor_string(row)
    urls = re.findall(fr'\s*{pattern}\s*', s)
    try:
        url = str(urls[0])
    except IndexError:
        url = ''
    return url


def refactor_string(row: str) -> str:
    row = re.sub(r'[\t,;]', ' ', row)
    row = row.strip()
    row = re.sub(r' {2,}', ' ', row)
    return row


def get_course_info_from_string(s: str) -> tuple:
    s = s.strip()
    try:
        couse_name = re.findall('(Курс: .*)\n', s)[0]
    except IndexError:
        couse_name = ''
    try:
        couse_teacher = re.findall('(Тренер:.*)\n', s)[0]
    except IndexError:
        couse_teacher = ''
    try:
        couse_date = re.findall('(Даты проведения курса:.*)\n', s)[0]
    except IndexError:
        couse_date = ''
    try:
        rows = s.split('\n')
        course = re.findall(r'(\w+-online)', rows[1].strip())[0]
        teacher = re.findall(r'Тренер:\s+([А-Яа-я]+)', rows[3].strip())[0]
        date = re.findall(r'Даты проведения курса:\s+([\d.\s\-]+)', rows[2].strip())[0]
        date = date.split('.')
        date = f'{datetime.date.today().strftime("%Y")}-{date[1].strip()}-{date[0].strip()}'

    except IndexError:
        course = ''
        date = ''
    return couse_name, couse_date,  couse_teacher, course
