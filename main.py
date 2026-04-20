import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.seed import seed
from app.metrics import start_metrics_server
from app.config import BOT_TOKEN
from app.data.connection import init_db, init_pool, close_pool
from app.handlers import profile, ai_client, tasks, base, theory

logging.basicConfig(level=logging.INFO)

bot_token = BOT_TOKEN


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in .env")
    bot = Bot(token=bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(base.router)
    dp.include_router(theory.router)
    dp.include_router(tasks.router)
    dp.include_router(profile.router)
    dp.include_router(ai_client.router)


    start_metrics_server(port=8000)
    await init_pool()
    await init_db()
    await seed()
    logging.info("Бот запущен")

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
        await bot.session.close()
        logging.info("Бот остановлен")

if __name__ == '__main__':
    asyncio.run(main())
