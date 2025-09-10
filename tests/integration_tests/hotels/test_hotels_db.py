from src.database import async_session_maker_null_pool
from src.schemas.hotels import SHotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db):
    hotel_data = SHotelAdd(title="Hotel 1", location="г.Сочи, ул. Морская, д. 32а")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel=}")