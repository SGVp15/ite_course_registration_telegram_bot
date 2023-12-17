from aiogram import types
from aiogram.dispatcher import filters

import webinar
from Config.config import USERS_ID, ADMIN_ID, PATTERN_ZOOM_REGISTRATION_URL, PATTERN_WEBINAR_REGISTRATION_URL
from Config.config_private import WEBINAR_TOKENS
from Contact import parser
from converter import read_xlsx, read_xls
from keybords.inline import inline_kb_main
from loader import dp, bot
from queue import add_to_queue_file


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, user_id=[*ADMIN_ID, *USERS_ID])
async def handle_document(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id

    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Read the contents of the file
    await bot.download_file(file_path, destination_dir='./data')
    path = f'./data/{file_path}'
    s = ''
    if path.endswith('.xls'):
        s = read_xls(path)
    elif path.endswith('.xlsx'):
        s = read_xlsx(path)
    elif path.endswith('.txt'):
        with open(path, encoding='utf-8', mode='r') as f:
            s = f.read()

    text_message = ''
    users = parser.get_users_from_string(s)
    try:
        webinar_users = [user for user in users if user.webinar_eventsid != '']
        all_webinar_users = []
        for token in WEBINAR_TOKENS:
            w = webinar.api_get_.WebinarApi(token=token)
            all_webinar_users.extend(parser.get_users_from_string(w.get_all_registration_url()))
        new_webinar_users = [user for user in webinar_users if user not in all_webinar_users]
        if new_webinar_users:
            for token in WEBINAR_TOKENS:
                w = webinar.api_get_.WebinarApi(token=token)
                response = w.post_registration_users_list(users=new_webinar_users)

        zoom_users = [user for user in users if user.url_registration != '']
        for user in zoom_users:
            add_to_queue_file(user)
        text_message += f'{users[0].course}\nДобавил:\n'
        for user in new_webinar_users:
            text_message += f'{user.last_name} {user.first_name} \n'
        for user in zoom_users:
            text_message += f'{user.last_name} {user.first_name} \n'
        await message.answer(f'Файл обработал {file_path}\n{text_message}', reply_markup=inline_kb_main)
    except Exception as e:
        print(e)


@dp.message_handler(
    filters.Regexp(regexp=[PATTERN_ZOOM_REGISTRATION_URL, PATTERN_WEBINAR_REGISTRATION_URL]),
    user_id=[*ADMIN_ID, *USERS_ID])
async def add_users_zoom_to_file(message: types.Message):
    users = parser.get_users_from_string(message.text)
    if users:
        await message.answer('Контакт не корректен', reply_markup=inline_kb_main)
    else:
        await message.reply('Добавил в очередь', reply_markup=inline_kb_main)

        webinar_users = [u for u in users if u.webinar_eventsid != '']
        if webinar_users:
            for token in WEBINAR_TOKENS:
                w = webinar.api_get_.WebinarApi(token=token)
                all_webinar_users = get_users_from_string(w.get_all_registration_url())
                new_webinar_users = [u for u in webinar_users if u not in all_webinar_users]
                w.post_registration_users_list(users=new_webinar_users)

        zoom_users = [u for u in users if u.webinar_eventsid == '']
        for user in zoom_users:
            add_to_queue_file(user)
