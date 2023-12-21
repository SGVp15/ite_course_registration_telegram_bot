from dotenv import dotenv_values

config = dotenv_values('./Config/.env')

BOT_TOKEN = config['BOT_TOKEN']

ADMIN_ID = list(dotenv_values('./Config/.env_telegram_admin').keys())

user_id_email = dotenv_values('./Config/.env_manager_telegram_id_email')
USERS_ID = list(user_id_email.keys())
# ------------------------------------------------------------
#  Webinar
WEBINAR_TOKENS = list(dotenv_values('./Config/.env_webinar_token'))
# ------------------------------------------------------------
# Email
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']
