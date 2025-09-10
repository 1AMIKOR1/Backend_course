import json

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import (
    Base,
    engine_null_pool,
    async_session_maker_null_pool,
)
from src.main import app
from src.models import *
from src.schemas.hotels import SHotelAdd
from src.schemas.rooms import SRoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def fill_database(setup_database, db):
    with open("tests/hotels_mock.json", encoding="UTF-8") as file_in:
        hotels_from_file = json.load(file_in)
    with open("tests/rooms_mock.json", encoding="UTF-8") as file_in:
        rooms_form_file = json.load(file_in)

    hotels_data = [SHotelAdd.model_validate(hotel) for hotel in hotels_from_file]
    rooms_data = [SRoomAdd.model_validate(room) for room in rooms_form_file]
    new_hotels = await db.hotels.add_bulk(hotels_data)
    new_rooms = await db.rooms.add_bulk(rooms_data)
    await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={"email": "johnsmith@email.com", "password": "password"},
    )
