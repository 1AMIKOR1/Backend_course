from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, insert

from src.database import Base
from src.exceptions.booking import RoomNotAvailableException
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_free
from src.schemas.bookings import SBoookingAdd


class BookingsRepository(BaseRepository):
    model: BookingsModel = BookingsModel
    mapper = BookingDataMapper

    async def add_booking(self, booking_data: SBoookingAdd, hotel_id: int):

        rooms_ids_to_get = rooms_ids_free(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_booking: list[int] = (
            (await self.session.execute(rooms_ids_to_get)).scalars().all()
        )

        if booking_data.room_id in rooms_ids_to_booking:
            return await self.add(booking_data)
        else:
            raise RoomNotAvailableException(booking_data.room_id)

    async def get_bookings_with_today_chekin(self):

        query = select(self.model).filter(self.model.date_from == date.today())

        result = await self.session.execute(query)

        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]
