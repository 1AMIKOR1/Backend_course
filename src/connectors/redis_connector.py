import logging

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logging.info(f"Начинаю подключение к Redis host={self.host} port= {self.port}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Успешное подключение к Redis host={self.host} port= {self.port}")

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        await self.redis.delete(key)

    async def disconnect(self):
        if self.redis:
            await self.redis.aclose()
