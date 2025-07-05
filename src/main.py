from fastapi import FastAPI, Query, Body


import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.hotels.routers import router as hotels_router

from src.config import settings

app = FastAPI()

app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
