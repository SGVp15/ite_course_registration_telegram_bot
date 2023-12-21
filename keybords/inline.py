from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from Call_Back_Data import CollBackData as callBackData

inline_btn_logs = InlineKeyboardButton('Скачать Логи', callback_data=callBackData.download_logs)
inline_kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Скачать логи ZOOM', callback_data=callBackData.get_log), ],
    [InlineKeyboardButton(text='📩 Скачать логи Webinar', callback_data=callBackData.get_registration_webinar), ],

    [InlineKeyboardButton(text='📒  Скачать файл Продавцы', callback_data=callBackData.get_seller), ],
    [InlineKeyboardButton(text='📩 Показать очередь Zoom', callback_data=callBackData.show_queue), ],

    [InlineKeyboardButton(text='>> ZOOM >>', callback_data=callBackData.zoom_menu), ],
    [InlineKeyboardButton(text='>> Admin >>', callback_data=callBackData.admin_menu), ],
])

inline_kb_zoom = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Назад <<', callback_data=callBackData.back_to_main), ],
    [InlineKeyboardButton(text='💻 Конференции ZOOM', url='https://zoom.us/meeting#/'), ],
    [InlineKeyboardButton(text='📹 Записи ZOOM', url='https://zoom.us/recording/'), ],
    [InlineKeyboardButton(text='📒 Отчеты', url='https://zoom.us/account/report/user'), ],
])

inline_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Back <<', callback_data=callBackData.back_to_main), ],
    [InlineKeyboardButton(text='📒  Скачать Логи Программные', callback_data=callBackData.get_log_program), ],
    [InlineKeyboardButton(text='📩 ️ Отправить тестовое письмо', callback_data=callBackData.send_test_email), ],
    [InlineKeyboardButton(text='☠️ Очистить очередь регистрации', callback_data=callBackData.clear_queue), ],
    # [InlineKeyboardButton(text='☠️ Удалить Логи регистрации', callback_data=cb.clear_log), ],
    # [InlineKeyboardButton(text='☠️ Удалить Курсы', callback_data=cb.clear_course), ],
])

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True
                              ).add(KeyboardButton('help'))
