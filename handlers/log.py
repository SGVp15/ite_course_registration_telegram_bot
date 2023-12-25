from aiogram import types

from Call_Back_Data import CollBackData as callBackData
from Config.config import SELLERS, LOG_FILE, WEBINAR_LOG
from Config.config_private import USERS_ID, ADMIN_ID
from keybords.inline import inline_kb_main
from loader import dp, bot
from queue_zoom import get_queue, clear_queue
from webinar.api_get_ import get_all_registration_url


def is_empty_file(file) -> bool:
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.callback_query_handler(lambda c: c.data in [callBackData.show_queue, ], user_id=[*ADMIN_ID, *USERS_ID])
async def show_queue(callback_query: types.callback_query):
    await bot.send_message(chat_id=callback_query.from_user.id, text=get_queue(), reply_markup=inline_kb_main)


@dp.callback_query_handler(lambda c: c.data in [callBackData.get_log, callBackData.get_seller], user_id=[*ADMIN_ID, *USERS_ID])
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == 'get_seller':
        file = SELLERS
    elif query == 'get_log':
        file = LOG_FILE

    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'✅ Файл {file} пустой',
                               reply_markup=inline_kb_main)
    else:
        with open(file, "rb") as f:
            await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)


@dp.callback_query_handler(lambda c: c.data == callBackData.get_registration_webinar, user_id=[*ADMIN_ID, *USERS_ID])
async def get_file_registration_webinar(callback_query: types.callback_query):
    file = WEBINAR_LOG
    get_all_registration_url()
    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Очередь Webinar пустая',
                               reply_markup=inline_kb_main)
    else:
        with open(file, "rb") as f:
            await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)


@dp.callback_query_handler(lambda c: c.data == callBackData.clear_queue, user_id=[*ADMIN_ID, ])
async def clear_queue_file(callback_query: types.callback_query):
    clear_queue()
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_queue  Ok', reply_markup=inline_kb_main)


@dp.callback_query_handler(lambda c: c.data == callBackData.clear_log, user_id=[*ADMIN_ID, ])
async def clear_log_file(callback_query: types.callback_query):
    # TODO create function
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_log Ok', reply_markup=inline_kb_main)