from unittest import TestCase
from Contact import parser
from Webinar.registration import start_registration


class Test(TestCase):
    def test_start_registration(self):
        s = '''Курс:	«Основы ITIL® 4» Онлайн		
		ITILF4-online		
	Даты проведения курса:	26.02.2024 - 01.03.2024 с 10:00 до 14:00 мск		
	Тренер:	Сапегин Степан Борисович		
	Место проведения:	Webinar_1 до 12.06		
	Идентификатор конференции:	
	Код доступа:			
	Ссылка для регистрации:	https://my.mts-link.ru/event/754618867/1522013028/edit		
        Савушкин Григорий g.savushkin@itexpert.ru
        '''
        users = parser.get_list_users_from_string(s)
        start_registration(users)
        # self.fail()
