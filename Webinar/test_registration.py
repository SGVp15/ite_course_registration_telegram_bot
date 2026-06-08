from unittest import TestCase

from Contact import parser
from Webinar.registration import start_registration


class Test(TestCase):
    def test_start_registration(self):
        s = '''		Курс: 	«ITIL® 4. Управление услугами цифровой организации: высокоскоростные ИТ» Онлайн		
	HVIT-online		
Даты проведения курса: 	16.12.2024 - 20.12.2024 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)		
Тренер: 	Аношин Владимир Львович		
Место проведения: 	MTS-link1 12.06.2025 		
Идентификатор конференции:			
Код доступа:			
Ссылка для регистрации:	https://my.mts-link.ru/j/ITExpert/1343194997		
ФИО	Организация	Должность	e-mail
Афыв Виовфыв Лвф	Abramova.VL@dd3.ru


        '''
        users = parser.get_list_users_from_string(s)
        start_registration(users)
