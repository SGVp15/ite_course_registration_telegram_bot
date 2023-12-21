from dotenv import dotenv_values

config = dotenv_values('./Config/.env')

BOT_TOKEN = config['BOT_TOKEN']

ADMIN_ID = [int(x) for x in config['ADMIN_ID'].split(',')]
USERS_ID = [int(x) for x in config['USERS_ID'].split(',')]
# ------------------------------------------------------------
#  Webinar
WEBINAR_TOKENS = [x.strip() for x in config['WEBINAR_TOKEN'].split(',')]
# ------------------------------------------------------------
# Email
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']