from unittest import TestCase

from Contact import User
from parser import get_users_from_string


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

        users = get_users_from_string(s)
        test_user = User(last_name='Савушкин', first_name='Григорий', email='g.savushkin@itexpert.ru',
                         url_registration='https://us06web.zoom.us/meeting/register/tZAscequpz0sGd0hMbssnWyDoB8nDJ4GeHfL')
        print('last_name', users[0].last_name == test_user.last_name)
        print('first_name', users[0].first_name == test_user.first_name)
        print('email', users[0].email == test_user.email)
        print('url_registration', users[0].url_registration == test_user.url_registration)
        print('webinar_eventsid', users[0].webinar_eventsid == test_user.webinar_eventsid)
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
1	Григорьева Сабина Ильдаровна		СТЭП ЛОДЖИК - Step Logic		(Сервис-менеджер,		s_grigoreva@step.ru	
2	Мосин Владимир Владимирович		Магнус Тех		Руководитель Москва		mosin@gkm.ru	
3	Смоленский Кирилл Викторович		Русагро Технологии				SmolenskyKV@MBNrs.ru	
4	Колодезникова Нарияна Евгеньевна		ER Tech Solutions				n.kolodeznikova@indriver.com	
5	Цветков Роман Владимирович		ER Tech Solutions				roman.tsvetkov@indriver.com	
6	Гаврильева Саина Вячеславовна		ER Tech Solutions				saina.gavrilyeva@indriver.com	
								
        """
        users = get_users_from_string(s)
        test_user = User(last_name='Григорьева', first_name='Сабина', email='s_grigoreva@step.ru',
                         url_registration='', webinar_eventsid='999146969')
        print(users[0])
        print(test_user)
        if users[0] != test_user:
            self.fail()

        if users[1] != User(last_name='Мосин', first_name='Владимир', email='mosin@gkm.ru',
                            url_registration='', webinar_eventsid='999146969'):
            self.fail()
        test_user = get_users_from_string("Григорьева	Сабина	s_grigoreva@step.ru	self.url_registration=''		self.webinar_eventsid='999146969'")[0]

        user = User(last_name='Григорьева', first_name='Сабина', email='s_grigoreva@step.ru',
                         url_registration='', webinar_eventsid='999146969')
        if test_user != user:
            self.fail()