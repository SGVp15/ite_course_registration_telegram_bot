from datetime import datetime
from unittest import TestCase

from Webinar import WebinarApi
from Webinar.config import WEBINAR_TOKENS
from Webinar.scheduler_records import scheduler_converter_records


class TestWebinarApi(TestCase):
    # def test_get_records_today(self):
    #     scheduler_converter_records()

    def test_get_records_today(self):
        record_id_list = []
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token)
            records = webinar_api.get_records_list()
            # records = webinar_api.get_records_list(from_date=datetime(2024, 12, 5))
            if records:
                for r in records:
                    try:
                        record_id = r.get('id')
                    except (TypeError, AttributeError):
                        record_id = None
                    if record_id and record_id not in record_id_list:
                        code, response = webinar_api.post_record_to_conversions(record_id)
                        if code == 200:
                            record_id_list.append(record_id)
                            print(f'[Records] {record_id} to converter = {response}')
                        else:
                            print(f'[Error] {response}')

    #     def test_get_events_ids_and_names_webinars_from_scheduler(self):
    #         for token in WEBINAR_TOKENS:
    #             webinar_api = WebinarApi(token)
    #
    #             a = webinar_api.get_events_ids_and_names_webinars_from_scheduler()
    #             print(a)
    #
    #     def test_get_all_registration_url(self):
    #         for token in WEBINAR_TOKENS:
    #             webinar_api = WebinarApi(token)
    #
    #         a = webinar_api.get_all_registration_url()
    #
    #     # def test_get_events_ids_and_names_webinars_from_scheduler(self):
    #     #     for token in WEBINAR_TOKENS:
    #     #         webinar_api = WebinarApi(token)
    #     #         webinar_api.get_events_ids_and_names_webinars_from_scheduler()
    #
    def test__parser_url(self):
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token)
            assert (webinar_api._parser_url('//////eventsessions//////participations//', s=234, a=2)
                    == 'https://userapi.mts-link.ru/v3/eventsessions/participations?s=234&a=2')

#
# def test_get_all_registration_url(self):
#     for token in WEBINAR_TOKENS:
#         webinar_api = WebinarApi(token)
#         s = webinar_api.get_all_registration_url()
#         print(s)
