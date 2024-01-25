from aiogram import types, F
from aiogram.types import FSInputFile

from Config.config import SELLERS, LOG_FILE, WEBINAR_LOG
from Telegram.Call_Back_Data import CallBackData
from Telegram.Call_Back_Data import CallBackData as callBackData
from Telegram.config import USERS_ID, ADMIN_ID
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from queue_zoom import get_queue, clear_queue
from Webinar.API import get_all_registration_url


def is_empty_file(file) -> bool:
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.callback_query(F.data.in_({callBackData.show_queue})
                   & F.user_id.in_({*ADMIN_ID, *USERS_ID}))
async def show_queue(callback_query: types.callback_query):
    await bot.send_message(chat_id=callback_query.from_user.id, text=get_queue(), reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({callBackData.get_log, callBackData.get_seller})
                   & F.user_id.in_({*ADMIN_ID, *USERS_ID}))
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == CallBackData.get_seller:
        file = FSInputFile(SELLERS, 'sellers.txt')
    elif query == CallBackData.get_log:
        file = FSInputFile(LOG_FILE, 'log_file.txt')

    # try:
    #     if is_empty_file(file):
    #         await bot.answer_callback_query(chat_id=callback_query.from_user.id, text=f'✅ Файл пустой',
    #                                         reply_markup=inline_kb_main)
    # except UnicodeDecodeError:
    #     ...
    await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({callBackData.get_registration_webinar})
                   & F.user_id.in_({*ADMIN_ID, *USERS_ID}))
async def get_file_registration_webinar(callback_query: types.callback_query):
    file = WEBINAR_LOG
    get_all_registration_url()
    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Очередь Webinar пустая',
                               reply_markup=inline_kb_main)
    else:
        with open(file, "rb") as f:
            await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({callBackData.clear_queue}) & F.user_id.in_({*ADMIN_ID}))
async def clear_queue_file(callback_query: types.callback_query):
    clear_queue()
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_queue  Ok', reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({callBackData.clear_log}) & F.user_id.in_({*ADMIN_ID}))
async def clear_log_file(callback_query: types.callback_query):
    # TODO create function
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_log Ok', reply_markup=inline_kb_main)
