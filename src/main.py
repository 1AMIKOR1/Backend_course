from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager

from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.auth import router as auth_router
from src.api.booking import router as booking_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    #При перезагрузке\выключении приложения
    await  redis_manager.disconnect()
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(booking_router)
app.include_router(facilities_router)
app.include_router(images_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
