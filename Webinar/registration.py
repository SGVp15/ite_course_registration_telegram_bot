from Contact import parser
from Email import EmailSending
from My_jinja import MyJinja
from Webinar.config import WEBINAR_TOKENS
from Webinar import WebinarApi
from Zoom.queue_zoom import get_old_users, add_to_queue_file


def start_registration(users):
    text_message = ''
    all_webinar_users = []
    webinar_users = [user for user in users if user.webinar_events_id != '']
    for token in WEBINAR_TOKENS:
        webinar_api = WebinarApi(token=token)
        all_webinar_users.extend(parser.get_users_from_every_row(webinar_api.get_all_registration_url()))
    new_webinar_users = [user for user in webinar_users if user not in all_webinar_users]

    if new_webinar_users:
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token=token)
            response = webinar_api.post_registration_users_list(users=new_webinar_users)
            print(response)
        # get all_webinar_users
        all_webinar_users = []
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token=token)
            all_webinar_users.extend(parser.get_users_from_every_row(webinar_api.get_all_registration_url()))
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
                EmailSending(subject=user.webinar_name,
                             to=user.email,
                             cc=user.curator_email,
                             bcc=user.manager_email,
                             text=text,
                             html=html,
                             manager=user.manager_email).send_email()
            else:
                EmailSending(subject=user.webinar_name,
                             to=user.email,
                             cc=user.curator_email,
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
