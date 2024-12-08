from unittest import TestCase

from Contact import parser
from Webinar.registration import start_registration


class Test(TestCase):
    def test_start_registration(self):
        s = '''		Курс:	«Бизнес-анализ. Управление требованиями к ПО» Онлайн		
		BASRM-online		
	Даты проведения курса:	26.11.2024 - 28.11.2024 с 10:00 до 14:30 мск		
	Тренер:	Алдонин Сергей Владимирович		
	Место проведения:	Webinar_3 до 03.03		
	Идентификатор конференции:			
	Код доступа:			
	Ссылка для регистрации:	https://my.mts-link.ru/j/81296985/1588102103		
	        Савушкин Григорий g.savushkin@itexpert.ru
        '''
        users = parser.get_list_users_from_string(s)
        start_registration(users)
