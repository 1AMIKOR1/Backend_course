from pydantic import BaseModel
from database import Base
from models.bookings import BookingsModel
from repositories.base import BaseRepository
from schemas.bookings import SBookingGet


class BookingsRepository(BaseRepository):
    model: Base = BookingsModel
    schema: BaseModel = SBookingGet

    # async def get_all(self, limit, offset) -> list[BaseModel]:
    #     query = select(self.model)
    #     query = query.limit(limit).offset(offset)
    #     result = await self.session.execute(query)
    #     result = [self.schema.model_validate(model) for model in result.scalars().all()]
    #     return result