from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']
