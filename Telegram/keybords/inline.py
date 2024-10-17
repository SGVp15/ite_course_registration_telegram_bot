import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Telegram.Call_Back_Data import CallBackData
from Telegram.config import DOCUMENTS

inline_btn_logs = InlineKeyboardButton(text='Скачать Логи', callback_data=CallBackData.download_logs)
inline_kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📄 Скачать Логи ZOOM', callback_data=CallBackData.get_log), ],
    [InlineKeyboardButton(text='📄 Скачать логи Webinar', callback_data=CallBackData.get_registration_webinar), ],

    [InlineKeyboardButton(text='📦 Скачать файл Продавцы', callback_data=CallBackData.get_seller), ],
    [InlineKeyboardButton(text='📒 Показать входящие файлы', callback_data=CallBackData.show_list_file), ],
    [InlineKeyboardButton(text='🧑‍💻 Показать очередь Zoom', callback_data=CallBackData.show_queue), ],
    [InlineKeyboardButton(text='📩 ️ Отправить тестовое письмо', callback_data=CallBackData.send_test_email), ],

    [InlineKeyboardButton(text='>> ZOOM >>', callback_data=CallBackData.zoom_menu), ],
    [InlineKeyboardButton(text='>> Admin >>', callback_data=CallBackData.admin_menu), ],
])

inline_kb_zoom = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💻 Конференции ZOOM', url='https://zoom.us/meeting#/'), ],
    [InlineKeyboardButton(text='📹 Записи ZOOM', url='https://zoom.us/recording/'), ],
    [InlineKeyboardButton(text='📒 Отчеты', url='https://zoom.us/account/report/user'), ],
    [InlineKeyboardButton(text='🔙 Назад', callback_data=CallBackData.back_to_main_menu), ],

])

inline_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📒 Скачать Логи Программные', callback_data=CallBackData.get_log_program), ],

    [InlineKeyboardButton(text='☠️ Очистить очередь регистрации', callback_data=CallBackData.clear_queue), ],
    [InlineKeyboardButton(text='☠️ Удалить Логи регистрации', callback_data=CallBackData.clear_log), ],
    [InlineKeyboardButton(text='🔙 Назад', callback_data=CallBackData.back_to_main_menu), ],

])


def get_list_files_keyboard(path=DOCUMENTS) -> [InlineKeyboardButton]:
    out_buttons = []
    files = os.listdir(path)
    for file in files:
        out_buttons.append(
            [
                InlineKeyboardButton(text=f'⏬ {file}', callback_data=f'file_download_{file}'),
                InlineKeyboardButton(text=f'🗑 {file}', callback_data=f'file_delete_{file}'),
            ]
        )
    out_buttons.append([InlineKeyboardButton(text='<< Back <<', callback_data=CallBackData.back_to_main_menu), ], )
    return InlineKeyboardMarkup(inline_keyboard=[*out_buttons])
