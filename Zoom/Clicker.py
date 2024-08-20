import asyncio
from datetime import datetime

from Config.config import LOG_FILE
from Utils.log import log
from Zoom.queue_zoom import Queue, load_old_users, save_old_users
from Zoom.selenium_zoom import registration_user_zoom_link


async def run_clicker():
    log.warning('webdriver run')
    while True:
        my_queue = Queue()
        try:
            user = my_queue.users[0]
        except IndexError:
            await asyncio.sleep(5)
            continue

        old_users = load_old_users()
        if user in old_users:
            log.info(f'[ INFO ] [ Есть в логе ] {user}')
            my_queue.del_user(user)
        else:
            log.info(f'[ INFO ] {user}')
            if await registration_user_zoom_link(user):
                save_old_users(user)

                write_user_to_log(f'{datetime.now()}\t{user}\n')
                log.info(f'[ OK ] {user}')
                my_queue.del_user(user)
            await asyncio.sleep(60 * 1)


def write_user_to_log(s):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(s)
