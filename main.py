import asyncio

from selenium import webdriver

from Telegram.main import start_bot
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.git_update import git_update
from Utils.log import log
from Webinar.sheduler_records import scheduler_converter_records
from Zoom.Clicker import run_clicker


async def main():
    tasks = [
        git_update(),
        start_bot(),
        run_clicker(),
        scheduler_converter_records(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    ChromedriverAutoupdate(operatingSystem="win").check()

    try:
        log.info('course registration bot START')
        asyncio.run(main())
    finally:
        log.error('course registration bot STOP')
