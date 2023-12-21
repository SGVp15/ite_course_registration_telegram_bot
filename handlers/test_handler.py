from aiogram import types

from Call_Back_Data import CollBackData as callBackData
from Config.config_private import USERS_ID, ADMIN_ID, user_id_email
from Contact import parser
from Email.email_sending import EmailSending
from keybords.inline import inline_kb_main
from loader import dp, bot


@dp.callback_query_handler(lambda c: c.data == callBackData.send_test_email, user_id=[*ADMIN_ID, *USERS_ID])
async def send_test_email_handler(callback_query: types.callback_query):
    s = '''Курс:	«ТЕСТ ТЕСТОнлайн						
		OPS-online						
	Даты проведения курса:	99.99.2000 - 80.90.2003 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)						
	Тренер:	Сапегин Степан Борисович						
	Место проведения:	Webinar_1						
	Идентификатор конференции:	+						
	Код доступа:							
	Ссылка для регистрации:	https://events.webinar.ru/event/999146969/1581189808/edit						
№	ФИО		Организация		Должность		e-mail	
1	Григорьева Сабина 					asdasdqdq@stadasdep.rasdasdu	'''

    user = parser.get_list_users_from_string(s)

    try:
        user.manager_email = user_id_email[str(callback_query.from_user.id)]
    except KeyError as e:
        print(e)

    template_html = MyJinja()
    html = template_html.create_document(user)

    template_text = MyJinja(template_file='course_registration.txt')
    text = template_text.create_document(user)

    text_message = EmailSending(subject=user.webinar_name, to=user.manager_email, text=text, html=html).send_email()
    await bot.send_message(chat_id=callback_query.from_user.id, text=text_message, reply_markup=inline_kb_main)
