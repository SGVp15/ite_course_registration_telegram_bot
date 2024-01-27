from aiogram import types, F

from Telegram.Call_Back_Data import callBackData
from Telegram.config import ADMIN_ID, USERS_ID
from Telegram.keybords.inline import inline_kb_admin, inline_kb_main, inline_kb_zoom
from Telegram.main import dp, bot


@dp.callback_query((F.data == callBackData.zoom_menu) & (F.from_user.id.in_({*ADMIN_ID, *USERS_ID})))
# @dp.callback_query()
async def zoom_menu(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_zoom)


@dp.callback_query((F.data == callBackData.admin_menu) & (F.from_user.id.in_({*ADMIN_ID})))
async def admin_menu(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_admin)


@dp.callback_query(F.data.in_(callBackData.back_to_main_menu))
# @dp.callback_query(F.data == callBackData.back_to_main_menu)
async def back_to_main(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_main)
