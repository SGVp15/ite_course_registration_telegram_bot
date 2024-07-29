from aiogram import types

from Telegram.main import dp, bot


@dp.callback_query()
async def echo(callback_query: types.callback_query):
    text = f'Не понимаю, что это значит.\nВоспользуйтесь командой /help'
    await bot.send_message(chat_id=callback_query.from_user.id, text=text)


@dp.message()
async def echo(message: types.Message):
    await message.reply(f'Не понимаю, что это значит.\nВоспользуйтесь командой /help')
