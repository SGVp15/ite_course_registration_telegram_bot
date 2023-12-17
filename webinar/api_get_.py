import time
from datetime import datetime

import requests

import Contact
from Config.config import WEBINAR_TOKENS


class WebinarApi:
    """
    url: https://userapi.webinar.ru/v3/eventsessions/{eventsessionsID}/participations?page=1&perPage=50,
    method: GET,
    headers:
    {
        x-auth-token: {Token},
        Content-Type: application/x-www-form-urlencoded
    };
    """

    def __init__(self, token):
        self.token = token
        self.headers = {'x-auth-token': self.token, 'Content-Type': 'application/x-www-form-urlencoded'}

    def get_response(self, url: str):
        r = requests.get(url, headers=self.headers)
        return r.json()

    # noinspection PyPep8Naming
    def get_url_client(self, event_sessions_id, events_id: str) -> str:
        # Вывод всех слушателей можно забрать индивидуальные ссылки url
        request = f'https://userapi.webinar.ru/v3/eventsessions/{event_sessions_id}/participations'
        base = 'https://events.webinar.ru/ITExpert'
        r = self.get_response(request)
        s = ''
        for row in r:
            s += f"{row['secondName']}, {row['name']}, {row['email']}, {base}/{events_id}/{row['url']}\n"
        return s

    @staticmethod
    def get_old_webinars_from_sheduler(from_date):
        # Вывод прошедших вебинаров
        request = f'https://userapi.webinar.ru/v3/stats/events?from={from_date}'
        r = get_response(request)
        for row in r:
            print('[name] = ', row['eventSessions'][0]['name'])
            print('[eventSessionsId] = ', row['eventSessions'][0]['id'])
            # pprint(row)
            print('')

    # noinspection PyPep8Naming
    def get_new_webinars_from_sheduler(self, from_date='', is_start_webinar=0):
        # Вывод всех вебинаров можно забрать [eventsessionsID]
        # eventId - для формирования полной ссылки
        # request = f'https://userapi.webinar.ru/v3/organization/events/schedule?perPage=250&page=1&status[2]=START&from={from_date}&to=2022-12-30'
        status_start = ''
        if is_start_webinar:
            status_start = 'status[2]=START&'

        url = f'https://userapi.webinar.ru/v3/organization/events/schedule?{status_start}from={from_date}'

        if from_date == '':
            url = f'https://userapi.webinar.ru/v3/organization/events/schedule?{status_start}'
        # request = f'https://userapi.webinar.ru/v3/organization/events/schedule'
        response = self.get_response(url=url)
        eventsId = {}
        name = {}
        for row in response:
            eventSessionsId = row['eventSessions'][0]['id']
            eventId = row['id']
            eventsId[eventSessionsId] = eventId
            name[eventSessionsId] = row['name']
        return eventsId, name

    # noinspection PyPep8Naming
    def print_link(self, event_sessions_id, event_id):
        s = self.get_url_client(event_sessions_id, event_id)
        l = s.split('\n')
        l.sort()
        return '\n'.join(l)

    def get_all_registration_url(self):
        now = datetime.now()
        from_date = now.strftime("%Y-%m-%d+00:00:00")
        is_start_webinar = 0

        events_ids, names = self.get_new_webinars_from_sheduler(from_date, is_start_webinar)
        out = ''
        for eventSessionsID in events_ids:
            event_id = events_ids[eventSessionsID]
            out += f'{names[eventSessionsID]}'
            # print(f'Ссылки слушателям')
            out += self.print_link(eventSessionsID, event_id)
            out += '\n'
            out += ('--' * 70)
            out += '\n'
        return out

    def post_registration_users_list(self, users: list[Contact], send_email_webinar_api='true'):
        # https://events.webinar.ru/event/999146969/1581189808/edit
        data = {'isAutoEnter': 'true',
                'sendEmail': 'true'}
        url = ''
        i = 0
        for user in users:
            url = f'https://userapi.webinar.ru/v3/events/{user.webinar_eventsid}/invite'
            if (i + 1) % 40 == 0:
                r = requests.post(url, headers=self.headers, data=data)
                # [{"participationId":752414983,"email":"g.savushkin@itexpert.ru","link":"https:\/\/my.mts-link.ru\/81296985\/569285096\/7ca38749207b4313ca9c9a420fefcdee"}]
                print(r.text)
                i = 0
                time.sleep(0.5)
                data = {'isAutoEnter': 'true',
                        'sendEmail': f'{send_email_webinar_api}'}

            data[f'users[{i}][email]'] = user.email
            data[f'users[{i}][name]'] = user.first_name
            data[f'users[{i}][secondName]'] = user.last_name
            data[f'users[{i}][role]'] = 'GUEST'
            i = i + 1
        r = requests.post(url, headers=self.headers, data=data)
        # [{"participationId":752414983,"email":"g.savushkin@itexpert.ru","link":"https:\/\/my.mts-link.ru\/81296985\/569285096\/7ca38749207b4313ca9c9a420fefcdee"}]
        print(r.text)
        return r.text


def get_all_registration_url():
    with open('./data/webinar_registration.txt', encoding='utf_8', mode='w') as f:
        for token in WEBINAR_TOKENS:
            w = WebinarApi(token=token)
            f.write(w.get_all_registration_url())
