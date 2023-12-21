from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

inline_btn_logs = InlineKeyboardButton('Скачать Логи', callback_data='download_logs')
inline_kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Скачать логи ZOOM', callback_data='get_log'),],
    [InlineKeyboardButton(text='📩 Скачать логи Webinar', callback_data='get_registration_webinar'), ],

    [InlineKeyboardButton(text='📒  Скачать файл Продавцы', callback_data='get_seller'), ],
    [InlineKeyboardButton(text='📩 Показать очередь Zoom', callback_data='show_queue'), ],

    [InlineKeyboardButton(text='>> ZOOM >>', callback_data='zoom_menu'), ],
    [InlineKeyboardButton(text='>> Admin >>', callback_data='admin_menu'), ],
])

inline_kb_zoom = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Назад <<', callback_data='back_to_main'), ],
    [InlineKeyboardButton(text='💻 Конференции ZOOM', url='https://zoom.us/meeting#/'), ],
    [InlineKeyboardButton(text='📹 Записи ZOOM', url='https://zoom.us/recording/'), ],
    [InlineKeyboardButton(text='📒 Отчеты', url='https://zoom.us/account/report/user'), ],
])

inline_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Back <<', callback_data='back_to_main'), ],
    [InlineKeyboardButton(text='📩  Скачать Логи Программные', callback_data='get_log_program'), ],
    # [InlineKeyboardButton(text='☠️ Удалить Логи регистрации', callback_data='clear_log'), ],
    # [InlineKeyboardButton(text='☠️ Удалить Курсы', callback_data='clear_course'), ],
])

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True
                              ).add(KeyboardButton('help'))
