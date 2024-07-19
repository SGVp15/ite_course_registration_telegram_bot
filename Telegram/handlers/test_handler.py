from aiogram import types, F

from Telegram.Call_Back_Data import CallBackData
from Telegram.config import USERS_ID, ADMIN_ID
from Email.test_email_sending import TestEmailSending
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot


@dp.callback_query((F.data == CallBackData.send_test_email)
                   & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def send_test_email_handler(callback_query: types.callback_query):
    text_message = TestEmailSending.test_send_email(callback_query.from_user.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text_message, reply_markup=inline_kb_main)
