import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import router
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.database.models import async_main
from app.handlers import router
from app.admin import admin

load_dotenv()
token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')


async def main():
    await async_main()
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(router, admin)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bye!')
