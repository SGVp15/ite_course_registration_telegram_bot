from aiogram import types, F
from aiogram.filters import Command
from magic_filter import RegexpMode

from Contact import parser
from Telegram.config import USERS_ID, ADMIN_ID, user_id_email
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Webinar.registration import start_registration
from converter import read_xlsx, read_xls


@dp.message(F.document & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID})))
async def handle_document(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id

    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Read the contents of the file
    await bot.download_file(file_path, destination=f'./data/{file_path}')
    path = f'./data/{file_path}'
    s = ''
    if path.endswith('.xls'):
        s = read_xls(path)
    elif path.endswith('.xlsx'):
        s = read_xlsx(path)
    elif path.endswith('.txt'):
        with open(path, encoding='utf-8', mode='r') as f:
            s = f.read()

    users = parser.get_list_users_from_string(s)
    # manager emails
    for user in users:
        try:
            user.manager_email = user_id_email.get(str(message.from_id), '')
        except (AttributeError, KeyError):
            pass
    text = start_registration(users)
    await message.answer(f'Файл обработал {file_path}\n{text}', reply_markup=inline_kb_main)


@dp.message(
    (F.text.regexp(r'https://', mode=RegexpMode.SEARCH))
    & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
)
async def add_users_zoom_to_file(message: types.Message):
    users = parser.get_list_users_from_string(message.text)
    for user in users:
        try:
            user.manager_email = user_id_email.get(str(message.from_id), '')
        except (AttributeError, KeyError):
            pass
    text = start_registration(users)
    if users is None:
        await message.answer('Контакт не корректен', reply_markup=inline_kb_main)
    else:
        await message.reply(f'Добавил в очередь {text}', reply_markup=inline_kb_main)
