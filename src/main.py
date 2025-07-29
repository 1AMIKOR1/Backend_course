from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.auth import router as auth_router
from src.api.booking import router as booking_router
from src.api.facilities import router as facilies_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(booking_router)
app.include_router(facilies_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
