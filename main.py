import asyncio

from Clicker.Clicker import run_clicker
from Telegram.main import start_bot


async def main():
    tasks = [
        start_bot(),
        run_clicker(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # loop.call_soon(start_bot, loop)

    print('bot start')
    asyncio.run(main())
