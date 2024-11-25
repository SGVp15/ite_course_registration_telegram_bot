import os.path

from Config import WEBINAR_HISTORY
from Contact import parser, User, Contact
from Email import EmailSending
from My_jinja import MyJinja
from Utils.log import log
from Webinar import WebinarApi
from Webinar.config import WEBINAR_TOKENS
from Zoom.queue_zoom import load_old_users, Queue


def start_registration(users: list[User]) -> str:
    if users[0].webinar_events_id != '':
        s = start_registration_webinar(users)
        return s
    else:
        return start_registration_zoom(users)


def start_registration_webinar(users: list[User]) -> str:
    all_webinar_users = []
    webinar_users = [user for user in users if user.webinar_events_id != '']
    token = ''
    webinar_name = ''
    for _token in WEBINAR_TOKENS:
        webinar_api = WebinarApi(token=_token)
        events_ids, names, description = webinar_api.get_events_ids_and_names_webinars_from_scheduler()
        for events_id in events_ids.values():
            if users[0].webinar_events_id == str(events_id):
                webinar_name = names[events_id]
                token = _token
                break

    if token == '':
        return '\n\nПроверьте ссылку регистрации !!!'

    webinar_api = WebinarApi(token=token)
    all_webinar_users.extend(parser.get_users_from_every_row(webinar_api.get_all_registration_url()))
    if os.path.exists(WEBINAR_HISTORY):
        with open(WEBINAR_HISTORY, mode='r', encoding='utf-8') as f:
            all_webinar_users.extend(parser.get_users_from_every_row(f.read()))

    new_webinar_users: list[User] = [user for user in webinar_users if user not in all_webinar_users]

    for user in users:
        user.webinar_name = webinar_name
    text_message = 'Нет новых слушателей'
    if new_webinar_users:
        response = webinar_api.post_registration_users_list(users=new_webinar_users)
        log.info(response)

        # get all_webinar_users
        all_webinar_users = []
        all_webinar_users.extend(parser.get_users_from_every_row(webinar_api.get_all_registration_url()))

        # add link to new_webinar_users
        for user in new_webinar_users:
            for old_user in all_webinar_users:
                if user == old_user:
                    user.link = old_user.url_registration

        # send email
        send_email(new_webinar_users)

        text_message = ''
        text_message += f'{users[0].webinar_name}\nДобавил:\n'
        for user in new_webinar_users:
            text_message += f'{user.last_name} {user.first_name} \n'

    return text_message


def send_email(users: [Contact]):
    with open(WEBINAR_HISTORY, mode='a', encoding='utf-8') as f:
        for user in users:
            html = MyJinja().create_document(user)
            text = MyJinja(template_file='course_registration.txt').create_document(user)
            EmailSending(subject=user.webinar_name,
                         to=user.email,
                         cc=user.curator_email,
                         bcc=user.manager_email,
                         text=text,
                         html=html,
                         manager=user.manager_email).send_email()
            f.write(f'{str(user)}\n')


def start_registration_zoom(users: list[User]) -> str:
    # ZOOM add to registration queue
    zoom_users = [user for user in users if user.webinar_events_id == '']
    new_zoom_users = []
    if zoom_users:
        old_zoom_users = load_old_users()
        new_zoom_users = [user for user in zoom_users if user not in old_zoom_users]
        Queue().add_users(new_zoom_users)

    text_message = ''
    text_message += f'{users[0].course}\nДобавил в очередь:\n'

    for user in new_zoom_users:
        text_message += f'{user.last_name} {user.first_name} \n'

    return text_message
