from unittest import TestCase

from Contact import User
from parser import get_list_users_from_string


class TestParser_get_list_users_from_string(TestCase):
    def test_webinar_url(self):
        s = """		Курс:	«ИТ-поддержка: практики ITIL® 4 в действии» Онлайн						
        		OPS-online						
        	Даты проведения курса:	11.12.2023 - 15.12.2023 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)						
        	Тренер:	Сапегин Степан Борисович						
        	Место проведения:	Webinar_1						
        	Идентификатор конференции:	+						
        	Код доступа:							
        	Ссылка для регистрации:	https://events.webinar.ru/event/999146969/1581189808/edit						
        №	ФИО		Организация		Должность		e-mail	
        1	РЛРФАЙАйащршйа Сабина Рфв			(Сервис-менеджер,		asdqdq@asdep.ru	

                """
        self.assertEqual(len(get_list_users_from_string(s)), 1)
        self.assertEqual(get_list_users_from_string(s)[0],
                         User(last_name='РЛРФАЙАйащршйа', first_name='Сабина', email='asdqdq@asdep.ru',
                              url_registration='', webinar_events_id='999146969'))

    def test_zoom_url(self):
        s = '''	Курс: 	«ITIL® 4. Совместное создание ценности и организация взаимодействия поставщиков и потребителей» Онлайн
                  		DSV-online
                  	Даты проведения курса: 	18.12.2023 - 22.12.2023 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)
                  	Тренер: 	Сапегин Степан Борисович
                  	Место проведения: 	Webinar_3
                  	Идентификатор конференции:	569285096
                  	Код доступа:

                  	Ссылка для регистрации:	https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL
                  №	ФИО		Организация		Должность		e-mail
                  1	Савушкин Григорий Михайлович						g.savushkin@itexpert.ru ite@itexpert.ru
                  2    Лолофа Александра Лолофаафаца						ololyaaa@sib.ru https://us06web.zoom.us/meeting/register/tZA
                  '''

        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')

        test_user_2 = User(last_name='Лолофа', first_name='Александра', email='ololyaaa@sib.ru',
                           url_registration='https://us06web.zoom.us/meeting/register/tZA')

        users = get_list_users_from_string(s)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], test_user)
        self.assertEqual(users[1], test_user_2)
        print(users[0])

    def test_zoom_url2(self):
        s = '''	Курс: «Основы COBIT 2019» Онлайн COBIT2019F-online
Даты проведения курса: 02.09.2024 - 06.09.2024 с 10:00 до 14:00 мск
Тренер: Громаков Владимир Эдуардович
 https://us06web.zoom.us/meeting/register/tZcpf-itqjouHdXwsGIRW-WZTOpxRFgl4Au9 Савушкин Григорий g.savushkin@itexpert.ru
                  1	Савушкин Григорий Михайлович						g.savushkin@itexpert.ru ite@itexpert.ru
                  2    Лолофа Александра Лолофаафаца						ololyaaa@sib.ru https://us06web.zoom.us/meeting/register/tZA
                  '''

        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')

        test_user_2 = User(last_name='Лолофа', first_name='Александра', email='ololyaaa@sib.ru',
                           url_registration='https://us06web.zoom.us/meeting/register/tZA')

        users = get_list_users_from_string(s)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], test_user)
        self.assertEqual(users[1], test_user_2)
        print(users[0])

    def test_type(self):
        self.assertRaises(TypeError, get_list_users_from_string, 1)
        self.assertRaises(TypeError, get_list_users_from_string, ['asfs', ])
        self.assertRaises(TypeError, get_list_users_from_string, ('asd',))
