from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag
from redis.asyncio import Redis


class RedisThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, default_limit: int = 1):
        self.redis = redis
        self.default_limit = default_limit

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        limit = get_flag(data, "rate_limit") or self.default_limit
        user_id = event.from_user.id

        redis_key = f"throttle_msg:{user_id}"

        is_set = await self.redis.set(redis_key, 1, ex=limit, nx=True)

        if not is_set:
            return
        return await handler(event, data)
