import time
from datetime import datetime, timedelta

import requests

import Contact
from Utils.log import log
from Webinar.config import WEBINAR_TOKENS, WEBINAR_REGISTRATION_FILE


class WebinarApi:
    base = 'https://events.webinar.ru/ITExpert'
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
        self.headers = {'x-auth-token': self.token,
                        'Content-Type': 'application/x-www-form-urlencoded'}
        self.base_url = 'https://userapi.webinar.ru/v3'

    def get_response(self, url: str):
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_url_clients(self, event_sessions_id, events_id: str) -> str:
        # Вывод всех слушателей можно забрать индивидуальные ссылки url
        request = f'{self.base_url}/eventsessions/{event_sessions_id}/participations'
        r = self.get_response(request)
        s = ''
        for row in r:
            s += f"{row['secondName']}, {row['name']}, {row['email']}, {self.base}/{events_id}/{row['url']}\n"
        return s

    def get_old_webinars_from_scheduler(self, from_date):
        # Вывод прошедших вебинаров
        request = f'{self.base_url}/stats/events?from={from_date}'
        r = self.get_response(request)
        for row in r:
            log.info('[name] = ', row['eventSessions'][0]['name'])
            log.info('[eventSessionsId] = ', row['eventSessions'][0]['id'])
            log.info('')

    def get_events_ids_and_names_webinars_from_scheduler(self, from_date: str = None, is_start_webinar=0) -> (dict,
                                                                                                              dict,
                                                                                                              dict):
        """ Вывод всех вебинаров можно забрать [eventsessionsID] eventId - для формирования полной ссылки request =
        f'https://userapi.webinar.ru/v3/organization/events/schedule?perPage=250&page=1&status[2]=START&from={from_date}&to=2022-12-30'
        """
        if not from_date:
            now = datetime.now()
            from_date = now.strftime("%Y-%m-%d+00:00:00")

        status_start = ''
        if is_start_webinar:
            status_start = 'status[2]=START&'

        url = f'{self.base_url}/organization/events/schedule?{status_start}'
        if from_date:
            url += f'from={from_date}'

        response = self.get_response(url=url)
        events_ids = {}
        names = {}
        description = {}
        try:
            for row in response:
                event_sessions_id = row['eventSessions'][0]['id']
                event_id = row['id']
                events_ids[event_sessions_id] = event_id
                names[event_id] = row['name']
                description[event_id] = row['description']
        except TypeError:
            pass
        finally:
            return events_ids, names, description

    def print_link(self, event_sessions_id, event_id):
        s = self.get_url_clients(event_sessions_id, event_id)
        rows = s.split('\n')
        sorted(rows)
        return '\n'.join(rows)

    def get_all_registration_url(self) -> str:
        events_ids, names, description = self.get_events_ids_and_names_webinars_from_scheduler()
        out_str = ''
        for eventSessionsID in events_ids:
            event_id = events_ids[eventSessionsID]
            out_str += (f'{names[event_id]}\n'
                        f'{self.print_link(eventSessionsID, event_id)}\n')

            try:
                if description[event_id]:
                    out_str += f'{description[event_id]}\n'
            except KeyError:
                pass
            out_str += f'{('--' * 70)}\n'
        return out_str

    def post_registration_users_list(self, users: list[Contact], send_email_webinar_api='true'):
        # https://events.webinar.ru/event/999146969/1581189808/edit
        data = {'isAutoEnter': 'true',
                'sendEmail': 'false'}
        url = ''
        i = 0
        for user in users:
            url = f'{self.base_url}/events/{user.webinar_events_id}/invite'
            if (i + 1) % 40 == 0:
                r = requests.post(url, headers=self.headers, data=data)
                # [{"participationId":752414983,"email":"g.savushkin@itexpert.ru","link":"https:\/\/my.mts-link.ru\/81296985\/569285096\/7ca38749207b4313ca9c9a420fefcdee"}]
                log.info(r.text)
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
        log.info(r.text)
        return r.text

    def get_records_list(self, from_date=datetime.now(), to_date=None) -> [dict]:
        """https://help.mts-link.ru/article/19658
        {{webinar_url_base}}/records?from=2024-11-26&to=2024-11-27

        ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ
from — дата начала периода выборки.
Формат: yyyy-mm-dd hh:mm:ss.
Без этого параметра запрос отработает от текущей даты и времени.

ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ
id — ID онлайн-записи. Можно посмотреть запросом GET /fileSystem/files?parent=parentID, где parentID - идентификатор папки "Записи";

period — период выборки. Значения:
- day —  день;
- week —  неделя;
- month — месяц;
- year — год.
Значение по умолчанию: текущая дата и время.

to — дата окончания периода выборки.
Формат: yyyy-mm-dd hh:mm:ss.
По умолчанию: from + 1 год.

userId — ID сотрудника Организации.
Ограничивает выборку вебинарами одного из сотрудников команды.
ID можно получить запросом GET /organization/members.

offset — параметр для пагинации результата. Значения: 0, 10, 20, 30 и т.д.

Внимание!Offset необходим для изменения страницы результатов. При offset 0, будут выведены записи с 1-й по 10-ю. При offset 10, будут записи с 11 по 20 и т.д.

limit — параметр для определения количества отображаемых результатов. Без указания параметра выводиться 10 первых результатов.
Можно указать любое число в диапазоне от 1 до 500.

        """

        if not from_date:
            from_date = datetime(year=2024, month=12, day=2)
        if not to_date:
            to_date = from_date + timedelta(days=1)

        from_date = from_date.strftime('%Y-%m-%d')
        to_date = to_date.strftime('%Y-%m-%d')

        url = f'{self.base_url}/records?from={from_date}&to={to_date}'
        r = self.get_response(url)
        return r

    def post_record_to_conversions(self, id_record,
                                   data: dict = {"quality": "1080", "view": "none_novideo"}) -> (int, dict):

        """https://help.mts-link.ru/article/19654
        {{webinar_url_base}}/r,ecords/1165356647/conversions

        data = {"quality": "1080",
                "view": "none_novideo"}

        quality — качество сконвертированного видео. Значения:
        - 720 — конвертация в разрешении 1280х720;
        - 1080 — конвертация в разрешении 1920х1080.
        Значение по умолчанию: 720.

        view — выбор отображаемой вкладки. На записи может быть как вкладка с чатом, так и вкладка с вопросами. Значения:
        - chat — отображать в MP4-файле чат, боковую панель и видео ведущих;
        - questions — отображать в MP4-файле вопросы, боковую панель и видео ведущих;
        - minichat — отображать в MP4-файле чат и видео ведущих;
        - minichat_novideo — отображать в MP4-файле только чат;
        - none — отображать в MP4-файле только видео ведущих;
        - chat_novideo — отображать в MP4-файле боковую панель и чат;
        - questions_novideo — отображать в MP4-файле боковую панель и вопросы;
        - none_novideo — конвертировать MP4-файл без боковой панели, чата, вопросов и видео ведущих.
        Значение по умолчанию: chat.
        """

        url = f'{self.base_url}/records/{id_record}/conversions'
        r = requests.post(url, headers=self.headers, data=data)
        return r.status_code, r.json()


def get_all_registration_url():
    with open(WEBINAR_REGISTRATION_FILE, encoding='utf_8', mode='w') as f:
        for token in WEBINAR_TOKENS:
            w = WebinarApi(token=token)
            f.write(w.get_all_registration_url())
