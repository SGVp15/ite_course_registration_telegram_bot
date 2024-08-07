import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN = config.get('BOT_TOKEN')
ADMIN_ID = [822072027, ]

# USERS_ID = list(user_id_email.keys())
USERS_ID = [167572883, 263161488, 5226450762]

DOCUMENTS = os.path.join(os.getcwd(), 'data', 'documents')
PATH_DOWNLOAD_FILE: str = os.path.join(os.getcwd(), 'data')

os.makedirs(DOCUMENTS, exist_ok=True)
os.makedirs(PATH_DOWNLOAD_FILE, exist_ok=True)
