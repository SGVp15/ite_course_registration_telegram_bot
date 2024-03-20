import asyncio

from Zoom.Clicker import run_clicker


async def main():
    tasks = [
        run_clicker(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
