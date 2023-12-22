from aiogram import types

from Call_Back_Data import CollBackData as callBackData
from Config.config_private import USERS_ID, ADMIN_ID, user_id_email
from Contact import parser
from Email.email_sending import EmailSending
from My_jinja.my_jinja import MyJinja
from keybords.inline import inline_kb_main
from loader import dp, bot
from Email.test_email_sending import TestEmailSending


@dp.callback_query_handler(lambda c: c.data == callBackData.send_test_email, user_id=[*ADMIN_ID, *USERS_ID])
async def send_test_email_handler(callback_query: types.callback_query):
    text_message = TestEmailSending.test_send_email(callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text_message, reply_markup=inline_kb_main)
