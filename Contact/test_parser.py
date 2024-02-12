from unittest import TestCase

from Contact import User
from parser import get_list_users_from_string


class Test(TestCase):
    def test_get_users_from_string(self):
        s = '''	Курс: 	«ITIL® 4. Совместное создание ценности и организация взаимодействия поставщиков и потребителей» Онлайн
           		DSV-online
           	Даты проведения курса: 	18.12.2023 - 22.12.2023 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)
           	Тренер: 	Сапегин Степан Борисович
           	Место проведения: 	Webinar_3
           	Идентификатор конференции:	569285096
           	Код доступа:

           	Ссылка для регистрации:	https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL
           №	ФИО		Организация		Должность		e-mail
           1	Савушкин Григорий Михайлович		Сибинтек				g.savushkin@itexpert.ru ite@itexpert.ru
           2    Широковская Александра Александровна		Сибинтек				shirokovskayaaa@sibintek.ru
           '''

        users = get_list_users_from_string(s)
        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')
        print('last_name', users[0].last_name == test_user.last_name)
        print('first_name', users[0].first_name == test_user.first_name)
        print('email', users[0].email == test_user.email)
        print('url_registration', users[0].url_registration == test_user.url_registration)
        print('webinar_eventsid', users[0].webinar_events_id == test_user.webinar_events_id)
        if users[0] != test_user:
            self.fail()

        if users[1] != User(last_name='Широковская', first_name='Александра', email='shirokovskayaaa@sibintek.ru',
                            url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL'):
            self.fail()
        s = """		Курс:	«ИТ-поддержка: практики ITIL® 4 в действии» Онлайн						
		OPS-online						
	Даты проведения курса:	11.12.2023 - 15.12.2023 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)						
	Тренер:	Сапегин Степан Борисович						
	Место проведения:	Webinar_1						
	Идентификатор конференции:	+						
	Код доступа:							
	Ссылка для регистрации:	https://events.webinar.ru/event/999146969/1581189808/edit						
№	ФИО		Организация		Должность		e-mail	
1	Григорьева Сабина Ильдаровна			(Сервис-менеджер,		asdasdqdq@stadasdep.ru	


        """
        users = get_list_users_from_string(s)
        test_user = User(last_name='Григорьева', first_name='Сабина', email='asdasdqdq@stadasdep.ru',
                         url_registration='', webinar_events_id='999146969')
        print(users[0])
        print(test_user)
        if users[0] != test_user:
            self.fail()

        test_user = get_list_users_from_string(
            "Григорьева	Сабина	s_grigoreva@step.ru	self.url_registration=''		self.webinar_eventsid='999146969'")[
            0]

        user = User(last_name='Григорьева', first_name='Сабина', email='s_grigoreva@step.ru',
                    url_registration='', webinar_events_id='999146969')
        if test_user != user:
            self.fail()

        s = 'https://events.webinar.ru/ITExpert/569285096/a0413b7e540c11cb8aa93d8a1bdf5f76 Рыбалкин Александ a.rybalkin@itexpert.ru'
        users = get_list_users_from_string(s)
        print(users[0])

        test_user = get_list_users_from_string(
            "Савушкин, Григорий, g.savushkin@itexpert.ru, https://events.webinar.ru/ITExpert/569285096/7ca38749207b4313ca9c9a420fefcdee")[
            0]

        user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                    webinar_events_id='569285096')
        if test_user != user:
            self.fail()

        print(users[0])
