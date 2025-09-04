from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.database import Base
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import BookingDataMapper
from src.schemas.bookings import SBookingGet


class BookingsRepository(BaseRepository):
    model: BookingsModel = BookingsModel
    mapper = BookingDataMapper

    # async def get_all(self, limit, offset) -> list[BaseModel]:
    #     query = select(self.model)
    #     query = query.limit(limit).offset(offset)
    #     result = await self.session.execute(query)
    #     result = [self.schema.model_validate(model) for model in result.scalars().all()]
    #     return result

    async def get_bookings_with_today_chekin(self):

        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )

        result = await self.session.execute(query)

        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]