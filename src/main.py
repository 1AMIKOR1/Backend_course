import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import logging

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.auth import router as auth_router
from src.api.booking import router as booking_router
from src.api.facilities import router as facilities_router
from src.api.hotels import router as hotels_router
from src.api.images import router as images_router
from src.api.rooms import router as rooms_router

# from fastapi_cache.backends.inmemory import InMemoryBackend чтобы импользовать ОЗУ вместо Redis
from src.config import settings
from src.init import redis_manager

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("Fastapi cache initialized")
    yield
    # При перезагрузке\выключении приложения
    await redis_manager.disconnect()


if settings.MODE == "TEST":
    pass
    # FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(lifespan=lifespan, title="MyBookingApp")

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(booking_router)
app.include_router(facilities_router)
app.include_router(images_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
