import os

from aiogram import types, F
from aiogram.types import FSInputFile

from Config.config import SELLERS, LOG_FILE, WEBINAR_LOG, SYSTEM_LOG
from Telegram.Call_Back_Data import CallBackData
from Telegram.config import USERS_ID, ADMIN_ID
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Utils.log import log, backup_logs
from Webinar.registration import write_all_registration_url_to_file
from Zoom.queue_zoom import get_queue, clear_queue


def is_empty_file(file) -> bool:
    if not os.path.exists(file):
        return True
    try:
        with open(file=file, mode="r", encoding='utf-8') as f:
            s = f.read()
            return len(s) <= 1
    except UnicodeDecodeError:
        return False


@dp.callback_query((F.data == CallBackData.show_queue)
                   & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_queue(callback_query: types.callback_query):
    text = 'Очередь пустая'
    if users := get_queue():
        text = f'Очередь:\n'
        for i, user in enumerate(users):
            text += f'{i + 1} {user.abs_course} {user.last_name} {user.first_name} {user.email}\n'
    await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=inline_kb_main)


@dp.callback_query(F.data.in_({CallBackData.get_log,
                               CallBackData.get_seller,
                               CallBackData.get_log_program,
                               })
                   & F.from_user.id.in_({*ADMIN_ID,
                                         *USERS_ID,
                                         }))
async def get_file(callback_query: types.callback_query):
    query = callback_query.data

    file_path = ''
    if query == CallBackData.get_seller:
        file_path = SELLERS
    elif query == CallBackData.get_log:
        file_path = LOG_FILE
    elif query == CallBackData.get_log_program:
        file_path = SYSTEM_LOG

    file = FSInputFile(file_path, filename=os.path.basename(file_path))

    try:
        if is_empty_file(file.path):
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'✅ Файл пустой',
                                   reply_markup=inline_kb_main)
        else:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)
    except UnicodeDecodeError:
        log.error('UnicodeDecodeError')


@dp.callback_query((F.data == CallBackData.get_registration_webinar)
                   & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID})))
async def get_file_registration_webinar(callback_query: types.callback_query):
    file = WEBINAR_LOG
    write_all_registration_url_to_file()
    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Очередь Webinar пустая',
                               reply_markup=inline_kb_main)
    else:
        file = FSInputFile(WEBINAR_LOG, filename='webinar.log')
        await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)


@dp.callback_query((F.data == CallBackData.clear_queue) & (F.from_user.id.in_({*ADMIN_ID})))
async def clear_queue_file(callback_query: types.callback_query):
    clear_queue()
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_queue  Ok', reply_markup=inline_kb_main)


@dp.callback_query((F.data == CallBackData.clear_log) & (F.from_user.id.in_({*ADMIN_ID})))
async def clear_log_file(callback_query: types.callback_query):
    backup_logs()
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    await bot.send_message(chat_id=callback_query.from_user.id, text='clear_log Ok', reply_markup=inline_kb_main)
