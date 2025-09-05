from src.database import async_session_maker
from src.schemas.hotels import SHotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = SHotelAdd(title="Hotel 1", location="г.Сочи, ул. Морская, д. 32а")
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel=}")