import asyncio

from Utils.log import log
from Zoom.Clicker import run_clicker
from Telegram.main import start_bot


async def main():
    tasks = [
        start_bot(),
        run_clicker(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    log.warning('course registration bot start')
    asyncio.run(main())
# git pull https://github.com/SGVp15/course_registration_telegram_bot | python main.py
