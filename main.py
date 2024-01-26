import asyncio

from Clicker.Clicker import run_main
from Telegram.main import start_bot


async def main():
    tasks = [
        start_bot(),
        run_main(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print('bot start')
    asyncio.run(main())
