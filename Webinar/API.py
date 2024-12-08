import re
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
    __requests_exceptions = (
        requests.exceptions.RequestException,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    )

    def __init__(self, token):
        self.token = token
        self.headers = {'x-auth-token': self.token,
                        'Content-Type': 'application/x-www-form-urlencoded'}
        self.base_url = 'https://userapi.mts-link.ru/v3'

    def _parser_url(self, url: str, **query) -> str:
        s = self.base_url
        if url:
            s += f'/{url}'
        s = re.sub('/+$', '', s)

        if query:
            s += '?'
        for k, v in query.items():
            s += f'{str(k)}={str(v)}&'

        s = re.sub('&$', '', s)
        s = re.sub(r'(?<!:)/+', '/', s)
        return s

    def get_request(self, url: str) -> dict | None:
        try:
            r = requests.get(url, headers=self.headers)
            return r.json()
        except self.__requests_exceptions as e:
            print(f'requests.exceptions {e}')
            return None

    def post_request(self, url: str, data) -> dict | None:
        try:
            r = requests.post(url, headers=self.headers, data=data)
            return r.json()
        except self.__requests_exceptions as e:
            print(f'requests.exceptions {e}')
            return None

    def get_url_clients(self, event_sessions_id, events_id: str) -> str:
        # Вывод всех слушателей можно забрать индивидуальные ссылки url
        request = self._parser_url(f'/eventsessions/{event_sessions_id}/participations')
        r = self.get_request(request)
        s = ''
        for row in r:
            s += f"{row['secondName']}, {row['name']}, {row['email']}, {self.base}/{events_id}/{row['url']}\n"
        return s

    def get_events_ids_and_names_webinars_from_scheduler(self, from_date: str = None, to_date: str = '',
                                                         is_start_webinar=False) -> (dict,
                                                                                     dict,
                                                                                     dict):
        """ Вывод всех вебинаров можно забрать [eventsessionsID] eventId - для формирования полной ссылки request =
        f'https://userapi.webinar.ru/v3/organization/events/schedule?status[2]=START&from={from_date}'
        """
        query = {}

        if not from_date:
            now = datetime.now()
            from_date = now.strftime("%Y-%m-%d+00:00:00")
        query['from'] = from_date

        if to_date:
            query['to'] = to_date

        if is_start_webinar:
            query['status[2]'] = 'START'

        url = self._parser_url('/organization/events/schedule', **query)
        response = self.get_request(url=url)

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
                        f'{self.base}/{event_id}\n'
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
            url = self._parser_url(f'/events/{user.webinar_events_id}/invite')
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

        if not to_date:
            to_date = from_date + timedelta(days=1)

        from_date = from_date.strftime('%Y-%m-%d')
        to_date = to_date.strftime('%Y-%m-%d')

        query = {'from': from_date, 'to': to_date}
        url = self._parser_url('/records', **query)
        r = self.get_request(url)
        return r

    def post_record_to_conversions(self, id_record,
                                   data: dict | None = None) -> (int, dict):

        """https://help.mts-link.ru/article/19654
        {{webinar_url_base}}/r,ecords/1165356647/conversions

        По умолчанию:
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
        if not data:
            data: dict = {"quality": "1080", "view": "none_novideo"}
        url = self._parser_url(f'/records/{id_record}/conversions')
        r = requests.post(url, headers=self.headers, data=data)
        if requests:
            return r.status_code, r.json()
        else:
            return -1, {}


def get_all_registration_url():
    with open(WEBINAR_REGISTRATION_FILE, encoding='utf_8', mode='w') as f:
        for token in WEBINAR_TOKENS:
            w = WebinarApi(token=token)
            f.write(w.get_all_registration_url())
