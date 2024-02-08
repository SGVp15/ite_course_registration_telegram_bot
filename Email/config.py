from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']
user_id_email = dotenv_values('./Config/.env_manager_telegram_id_email')
email_login_password = dotenv_values('./Config/.env_email_login_password')
SMTP_SERVER = 'smtp.yandex.ru'
SMTP_PORT = 465
EMAILS_SALLER = ['a.katkov@itexpert.ru', 'a.rybalkin@itexpert.ru', 'g.savushkin@itexpert.ru']
