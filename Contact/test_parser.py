from unittest import TestCase

from Contact import User
from parser import get_list_users_from_string, refactor_string


class TestParser_get_list_users_from_string(TestCase):
    def test_webinar_url(self):
        s = """https://my.mts-link.ru/j/ITExpert/2007951276
                Савушкин Григорий g.savushkin@itexpert.ru
                """
        self.assertEqual(len(get_list_users_from_string(s)), 1)
        self.assertEqual(get_list_users_from_string(s)[0],
                         User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                              url_registration='', webinar_events_id='2007951276'))

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

        users = get_list_users_from_string(s)
        self.assertEqual(len(users), 2)

        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')

        test_user_2 = User(last_name='Лолофа', first_name='Александра', email='ololyaaa@sib.ru',
                           url_registration='https://us06web.zoom.us/meeting/register/tZA')

        self.assertEqual(users[0], test_user)
        self.assertEqual(users[1], test_user_2)
        print(users[0])

    def test_zoom_url_str(self):
        s = '''	Курс: «Основы COBIT 2019» Онлайн COBIT2019F-online
Даты проведения курса: 02.09.2024 - 06.09.2024 с 10:00 до 14:00 мск
Тренер: Громаков Владимир Эдуардович
 https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL Савушкин Григорий g.savushkin@itexpert.ru
                  '''

        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')

        users = get_list_users_from_string(s)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], test_user)
        print(users[0])

    def test_type(self):
        self.assertRaises(TypeError, get_list_users_from_string, 1)
        self.assertRaises(TypeError, get_list_users_from_string, ['asfs', ])
        self.assertRaises(TypeError, get_list_users_from_string, ('asd',))

# class Test(TestCase):
#     def test_get_list_users_from_string(self):
#         self.fail()
