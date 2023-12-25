from aiogram import types
from aiogram.dispatcher import filters

import webinar
from Config.config_private import USERS_ID, ADMIN_ID, WEBINAR_TOKENS, user_id_email
from Contact import parser
from Email.email_sending import EmailSending
from My_jinja.my_jinja import MyJinja
from converter import read_xlsx, read_xls
from keybords.inline import inline_kb_main
from loader import dp, bot
from queue_zoom import add_to_queue_file, get_old_users


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

    users = parser.get_list_users_from_string(s)
    for user in users:
        user.manager_email = user_id_email.get(str(message.from_id), '')
    text = start_registration(users)
    await message.answer(f'Файл обработал {file_path}\n{text}', reply_markup=inline_kb_main)


@dp.message_handler(filters.Regexp(regexp='https://'), user_id=[*ADMIN_ID, *USERS_ID])
async def add_users_zoom_to_file(message: types.Message):
    users = parser.get_list_users_from_string(message.text)
    for user in users:
        user.manager_email = user_id_email.get(str(message.from_id), '')
    text = start_registration(users)
    if users is None:
        await message.answer('Контакт не корректен', reply_markup=inline_kb_main)
    else:
        await message.reply(f'Добавил в очередь {text}', reply_markup=inline_kb_main)


def start_registration(users):
    text_message = ''
    all_webinar_users = []
    webinar_users = [user for user in users if user.webinar_events_id != '']
    for token in WEBINAR_TOKENS:
        webinar_api = webinar.api_get_.WebinarApi(token=token)
        all_webinar_users.extend(parser.get_users_from_event_row(webinar_api.get_all_registration_url()))
    new_webinar_users = [user for user in webinar_users if user not in all_webinar_users]

    if new_webinar_users:
        for token in WEBINAR_TOKENS:
            webinar_api = webinar.api_get_.WebinarApi(token=token)
            response = webinar_api.post_registration_users_list(users=new_webinar_users)
            print(response)
        # get all_webinar_users
        all_webinar_users = []
        for token in WEBINAR_TOKENS:
            webinar_api = webinar.api_get_.WebinarApi(token=token)
            all_webinar_users.extend(parser.get_users_from_event_row(webinar_api.get_all_registration_url()))
        # add link to new_webinar_users
        for user in new_webinar_users:
            for old_user in all_webinar_users:
                if user == old_user:
                    user.link = old_user.url_registration
        # send email
        for user in new_webinar_users:
            template_html = MyJinja()
            html = template_html.create_document(user)

            template_text = MyJinja(template_file='course_registration.txt')
            text = template_text.create_document(user)
            if user.manager_email != '':
                EmailSending(subject=user.webinar_name, from_email='Course', to=user.email, cc=user.curator_email,
                             bcc=user.manager_email,
                             text=text,
                             html=html,
                             manager=user.manager_email).send_email()
            else:
                EmailSending(subject=user.webinar_name, from_email='Course', to=user.email, cc=user.curator_email,
                             text=text,
                             html=html).send_email()

    # ZOOM add to registration queue
    zoom_users = [user for user in users if user.webinar_events_id == '']
    new_zoom_users = []
    if zoom_users:
        old_zoom_users = get_old_users()
        new_zoom_users = [user for user in zoom_users if user not in old_zoom_users]
        add_to_queue_file(new_zoom_users)

    text_message += f'{users[0].course}\nДобавил:\n'
    for user in new_webinar_users:
        text_message += f'{user.last_name} {user.first_name} \n'
    for user in new_zoom_users:
        text_message += f'{user.last_name} {user.first_name} \n'

    return text_message
