import asyncio
import logging
from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.exceptions import TelegramRetryAfter

class RetryRequestMiddleware(BaseRequestMiddleware):
    async def __call__(self, make_request, bot, method):
        try:
            return await make_request(bot, method)
        except TelegramRetryAfter as ex:
            logging.warning(f"Уперлись в лимиты API! Ждем {ex.retry_after} секунд...")
            await asyncio.sleep(ex.retry_after)
            return await make_request(bot, method)
