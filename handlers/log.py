from aiogram import types

from Config.config import USERS_ID, SELLERS, ADMIN_ID, QUEUE, LOG_FILE
from keybords.inline import inline_kb_main
from loader import dp, bot
from webinar.api_get_ import get_all_registration_url

def is_empty_file(file) -> bool:
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.callback_query_handler(
    lambda c: c.data in ['get_log', 'get_seller', 'get_courses', 'get_queue', 'get_history', 'get_log_program'],
    user_id=[*ADMIN_ID, *USERS_ID])
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == 'get_seller':
        file = SELLERS
    elif query == 'get_log':
        file = LOG_FILE
        # remove_sort_csv(file=file)
    # elif query == 'get_courses':
    #     file = COURSES_FILE
    elif query == 'get_queue':
        file = QUEUE
    # elif query == 'get_history':
    #     file = LOG_BACKUP
    # elif query == 'get_log_program':
    #     file = LOG_PROGRAM

    if is_empty_file(file):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'✅ Файл {file} пустой',
                               reply_markup=inline_kb_main)
    else:
        with open(file, "rb") as f:
            await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)


@dp.callback_query_handler(lambda c: c.data == 'get_registration_webinar', user_id=[*ADMIN_ID, *USERS_ID])
async def get_file_registration_webinar(callback_query: types.callback_query):
    file = './data/webinar_registration.txt'
    get_all_registration_url()
    with open(file, "rb") as f:
        await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)

# @dp.callback_query_handler(lambda c: c.data in ['clear_course', 'clear_log'], user_id=[*ADMIN_ID, ])
# async def clear_file(callback_query: types.callback_query):
#     query = callback_query.data
#
#     if query == 'clear_log':
#         file = LOG_FILE
#         file_backup = LOG_BACKUP
#     elif query == 'clear_course':
#         file = COURSES_FILE
#         file_backup = COURSES_FILE_BACKUP
#
#     backup_log(file=file, file_backup=file_backup)
#
#     with open(file=file, mode="w", encoding='utf-8') as f:
#         f.write('')
#     await bot.send_message(chat_id=callback_query.from_user.id, text='Ok', reply_markup=inline_kb_main)
