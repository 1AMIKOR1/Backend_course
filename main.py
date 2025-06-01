from fastapi import FastAPI, Query, Body
from hotels.routers import router as hotels_router

import uvicorn

app = FastAPI()

app.include_router(hotels_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)