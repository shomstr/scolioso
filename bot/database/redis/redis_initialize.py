from aiomysql.cursors import DictCursor
from aiomysql.pool import Pool
from redis import Redis

import asyncio


async def redis_initialize(pool: Pool, redis: Redis):
    async with pool.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            tasks = [load_restrict_bot_users(cur, redis)]
            await asyncio.gather(*tasks)
