import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv

from bot import dp
from loggers import logger


async def main() -> None:
    """
    Функция запускает бота
    """
    logger.info("[+] Bot is started")
    bot = Bot(TOKEN)
    await dp.start_polling(bot)
    logger.info("[+] Bot is stoped")


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    asyncio.run(main())
