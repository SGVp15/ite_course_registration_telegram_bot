import datetime
import re

from Config.config import PATTERN_ZOOM_REGISTRATION_URL, PATTERN_WEBINAR_REGISTRATION_URL
from Contact import User


def parsing_cyrillic(row) -> list:
    row = re.sub(r'[^ А-Яа-яЁё]+', '', row)
    cyrillic = re.findall(r'([А-Яа-яЁё]+)', row)
    return cyrillic


def get_users_from_string(s: str) -> list[User]:
    s = refactor_string(s)
    date, course, teacher = get_course_info_from_string(s)
    url = parsing_for_pattern(row=s, pattern=fr'\s*({PATTERN_ZOOM_REGISTRATION_URL})\s*')

    webinar_eventsid = parsing_for_pattern(row=s, pattern=fr'\s*{PATTERN_WEBINAR_REGISTRATION_URL}\s*')
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
                        webinar_eventsid=webinar_eventsid, curator_email=curator_email)
            user.date, user.course, user.teacher = date, course, teacher
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
    '''	Курс: 	«QA и тестирование программного обеспечения» Онлайн
             QA-online    
    Даты проведения курса: 	20.03 - 24.03.2023, 5 занятий с 11:00 до 15:00 мск (24 ак. часа)
    Тренер: 	Звездин Артем Сергеевич
    Место проведения: 	Zoom_1
    Идентификатор конференции:	873 5209 8606
    '''

    rows = s.split('\n')
    try:
        course = re.findall(r'(\w+-online)', rows[1].strip())[0]
        teacher = re.findall(r'Тренер:\s+([А-Яа-я]+)', rows[3].strip())[0]
        date = re.findall(r'Даты проведения курса:\s+([\d.\s\-]+)', rows[2].strip())[0]
        date = date.split('.')
        date = f'{datetime.date.today().strftime("%Y")}-{date[1].strip()}-{date[0].strip()}'
    except IndexError:
        return '', '', ''
    return date, course, teacher
