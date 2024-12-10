import os

from aiogram import types, F
from magic_filter import RegexpMode

from Contact import parser
from Email.config import user_id_email
from Excel.converter import read_xlsx, read_xls
from Telegram.config import USERS_ID, ADMIN_ID, PATH_DOWNLOAD_FILE
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Webinar.registration import start_registration


def add_seller_account(s):
    return f'{s}\nСавушкин\tГригорий\tg.savushkin@itexpert.ru'


@dp.message(F.document & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID})))
async def handle_document(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id

    # Download the file
    file = await bot.get_file(file_id)

    file_path = file.file_path
    path = os.path.join(PATH_DOWNLOAD_FILE, file_path)

    # Read the contents of the file
    await bot.download_file(file_path, destination=path)
    s = ''
    if path.endswith('.xls'):
        s = read_xls(path)
    elif path.endswith('.xlsx'):
        s = read_xlsx(path)
    elif path.endswith('.txt'):
        with open(path, encoding='utf-8', mode='r') as f:
            s = f.read()
            s = add_seller_account(s)

    users = parser.get_list_users_from_string(s)
    # manager emails
    for user in users:
        user.manager_email = user_id_email.get(str(message.from_user.id), '')

    text = start_registration(users)
    await message.answer(f'Файл обработал {file_path}\n{text}', reply_markup=inline_kb_main)


@dp.message(
    (F.text.regexp(r'https://', mode=RegexpMode.SEARCH))
    & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
)
async def add_users_zoom_to_file(message: types.Message):
    users = parser.get_list_users_from_string(add_seller_account(message.text))
    for user in users:
        user.manager_email = user_id_email.get(str(message.from_user.id), '')

    text = start_registration(users)
    if users is None:
        await message.answer('Контакт не корректен', reply_markup=inline_kb_main)
    else:
        await message.reply(text, reply_markup=inline_kb_main)
