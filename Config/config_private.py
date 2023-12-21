from dotenv import dotenv_values
from Config.manages_id_email import user_id_email

config = dotenv_values('./Config/.env')
BOT_TOKEN = config['BOT_TOKEN']

ADMIN_ID = [int(x) for x in config['ADMIN_ID'].split(',')]
USER_ID_EMAIL = user_id_email
USERS_ID = list(user_id_email.keys())
# ------------------------------------------------------------
#  Webinar
WEBINAR_TOKENS = [x.strip() for x in config['WEBINAR_TOKEN'].split(',')]
# ------------------------------------------------------------
# Email
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']