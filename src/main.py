import os
import asyncio

from aiogram import Bot
from dotenv import load_dotenv

from loggers import logger

from bot import dp, start_db


async def main() -> None:
    """
    Функция запускает бота
    """
    logger.info("[+] Start bot")
    bot = Bot(TOKEN)
    await start_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    asyncio.run(main())
