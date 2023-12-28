from unittest import TestCase

from Contact.parser import get_list_users_from_string
from My_jinja.my_jinja import MyJinja


class TestMyJinja(TestCase):
    def test_create_document(self):
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
        print(users)
        jin = MyJinja(template_folder='../Email/template_email')
        for i, user in enumerate(users):
            with open(f'./{i}.html', mode='w', encoding='utf-8') as f:
                f.write(jin.create_document(user))

        # self.fail()
