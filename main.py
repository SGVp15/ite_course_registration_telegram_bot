from Clicker.Clicker import run_main

from Telegram.main import dp, loop

if __name__ == '__main__':
    print('bot start')
    loop.create_task(run_main())
    executor.start_polling(dp)
