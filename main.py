from selenium import webdriver
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
    # driver = webdriver.Chrome()
    # driver.close()

    try:
        log.info('course registration bot START')
        asyncio.run(main())
    finally:
        log.error('course registration bot STOP')
# git pull https://github.com/SGVp15/course_registration_telegram_bot | python main.py
