import json

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import SHotelAdd
from src.schemas.rooms import SRoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session",autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session",autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
         await conn.run_sync(Base.metadata.drop_all)
         await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session",autouse=True)
async def fill_database(setup_database):
    with open("tests/hotels_mock.json", encoding="UTF-8") as file_in:
        hotels = json.load(file_in)
    with open("tests/rooms_mock.json", encoding="UTF-8") as file_in:
        rooms = json.load(file_in)

    hotels_data = [ SHotelAdd(**hotel) for hotel in hotels ]
    rooms_data = [ SRoomAdd(**room) for room in rooms ]
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotels = await db.hotels.add_bulk(hotels_data)
        new_rooms = await db.rooms.add_bulk(rooms_data)
        await db.commit()
        print(f"{new_hotels=}")
        print(f"{new_rooms=}")
@pytest.fixture(scope="session",autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "johnsmith@email.com",
                "password": "password"
            }
        )