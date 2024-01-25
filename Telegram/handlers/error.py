from aiogram import types
from aiogram.filters import Command

from Telegram.main import dp


@dp.message(Command('error'))
async def echo(message: types.Message):
    await message.reply('error Не понимаю, что это значит.'
                        'Воспользуйтесь командой /help')
    with open(f'./log.txt', encoding='utf-8', mode='a') as f:
        for k, v in message:
            f.write(f'{k} {v}', )
        f.write('\n')
