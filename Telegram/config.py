from dotenv import dotenv_values, load_dotenv, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN: str | None = config.get('BOT_TOKEN')
ADMIN_ID = [822072027, ]
user_id_email = dotenv_values('./Config/.env_manager_telegram_id_email')
# USERS_ID = list(user_id_email.keys())
USERS_ID = [167572883, 263161488, 5226450762]

email_login_password = dotenv_values('./Config/.env_email_login_password')
# ------------------------------------------------------------
#  Webinar
WEBINAR_TOKENS = list(dotenv_values('./Config/.env_webinar_token'))
# ------------------------------------------------------------
# Email
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']
