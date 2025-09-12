import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv('.env'))

BOT_TOKEN = config.get('BOT_TOKEN')
ADMIN_ID = config.get('ADMIN_ID').split(',')
ADMIN_ID = [w.strip() for w in ADMIN_ID]
# USERS_ID = list(user_id_email.keys())
USERS_ID = config.get('USERS_ID').split(',')
USERS_ID = [w.strip() for w in USERS_ID]
DOCUMENTS = os.path.join(os.getcwd(), 'data', 'documents')
PATH_DOWNLOAD_FILE: str = os.path.join(os.getcwd(), 'data')

os.makedirs(DOCUMENTS, exist_ok=True)
os.makedirs(PATH_DOWNLOAD_FILE, exist_ok=True)
