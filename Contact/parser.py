import datetime
import re

from Config.config import PATTERN_URL, PATTERN_WEBINAR_EVENT_ID
from Contact import User


def parsing_cyrillic(row) -> list:
    row = re.sub(r'[^ А-Яа-яЁё]+', '', row)
    cyrillic = re.findall(r'([А-Яа-яЁё]+)', row)
    return cyrillic


def get_users_from_every_row(s: str) -> list[User]:
    users = []
    for row in s.split('\n'):
        users.extend(get_list_users_from_string(row))
    return users


def get_list_users_from_string(s: str) -> list[User]:
    if type(s) is not str:
        raise TypeError('Input string must be string')

    s = refactor_string(s)
    course_name, date, teacher = get_course_info_from_string(s)
    first_url = parsing_for_pattern(string=s, pattern=PATTERN_URL)

    webinar_name = ''
    try:
        first_webinar_events_id = re.findall(pattern=PATTERN_WEBINAR_EVENT_ID, string=first_url)[0][1]
        webinar_name = course_name
    except IndexError:
        first_webinar_events_id = ''

    rows = s.split('\n')

    users = []
    for row in rows:
        emails = re.findall(r'(\S*@\S*)', row)
        row = re.sub(r'(\S*@\S*)', '', row)
        if not emails:
            continue

        url = parsing_for_pattern(string=row, pattern=PATTERN_URL)
        if url:
            try:
                webinar_events_id = re.findall(pattern=PATTERN_WEBINAR_EVENT_ID, string=first_url)[0][1]
            except IndexError:
                webinar_events_id = ''
        else:
            url = first_url
            webinar_events_id = first_webinar_events_id

        curator_email = ''
        if len(emails) > 1:
            curator_email = emails[1]
        email = emails[0]
        email = re.sub(r'[^@\w_\-.]', '', email.lower())

        row = re.sub(r'(\S*@\S*)', '', row)
        row = re.sub(r'[^A-Za-z А-Яа-яЁё]+', '', row)
        name = parsing_cyrillic(row)
        try:
            user = User(last_name=name[0], first_name=name[1], email=email, url_registration=url, course=course_name,
                        webinar_events_id=webinar_events_id, curator_email=curator_email,
                        webinar_name=webinar_name,
                        date=date, teacher=teacher)
            users.append(user)
        except IndexError:
            pass
    return users


def parsing_for_pattern(string: str, pattern: str) -> str:
    s = refactor_string(string)
    urls = re.findall(pattern, s)
    try:
        url = urls[0]
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
        course_name = re.findall('Курс:(.*)\n', s)[0].strip()
    except IndexError:
        course_name = ''
    try:
        course_teacher = re.findall('Тренер:(.*)\n', s)[0].strip()
    except IndexError:
        course_teacher = ''
    try:
        course_date = re.findall('Даты проведения курса:(.*)\n', s)[0].strip()
    except IndexError:
        course_date = ''

    # rows = s.split('\n')
    # try:
    #     course = 'Курс: ' + re.findall(r'(\w+-online)', rows[1].strip())[0]
    # except IndexError:
    #     course = ''

    return course_name, course_date, course_teacher  # , course
