
import asyncio
import os
import sys
import asyncpg
from redis.asyncio import Redis

async def check():
    try:

        conn = await asyncpg.connect(
        user=os.getenv("DB_USER", "postgres"),
         password=os.getenv("DB_PASS", "postgres"),
        database=os.getenv("DB_NAME", "postgres"),
        host=os.getenv("DB_HOST", "db"), # Обращаемся по внутреннему имени Докера
        port=5432,
        timeout=5
        )
        await conn.execute("SELECT 1")
        await conn.close()
        print("✅PostgreSQL")

        redis = Redis(host="redis", port=6379, socket_timeout=5)
        await redis.ping()
        await redis.aclose()
        print("✅Redis")

        sys.exit(0)

    except Exception as ex:
        print(f"❌ ОШИБКА {ex}")
        sys.exit(1)

if __name__ == "__main__":
  asyncio.run(check())