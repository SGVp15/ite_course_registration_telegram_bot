import asyncio

from selenium import webdriver

from Telegram.main import start_bot
from Utils.log import log
from Zoom.Clicker import run_clicker


async def main():
    tasks = [
        start_bot(),
        run_clicker(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.close()

    try:
        log.info('course registration bot START')
        asyncio.run(main())
    finally:
        log.error('course registration bot STOP')
