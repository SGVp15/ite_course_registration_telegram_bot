import os.path

from dotenv import dotenv_values

WEBINAR_TOKENS = list(dotenv_values('./Webinar/.env_webinar_token'))

WEBINAR_REGISTRATION_FILE = os.path.join(os.getcwd(), 'data', 'webinar_registration.txt')
