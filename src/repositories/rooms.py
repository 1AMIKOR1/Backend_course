from pydantic import BaseModel
from sqlalchemy import func, select
from database import Base
from repositories.base import BaseRepository
from models.rooms import RoomsModel
from schemas.rooms import SRoomGet


class RoomsRepository(BaseRepository):
    model: Base = RoomsModel
    schema: BaseModel = SRoomGet

    async def get_all(self, hotel_id, price, title, limit, offset):
        query = select(self.model)
        if hotel_id:
            query = query.filter(self.model.hotel_id == hotel_id)

        if price:
            query = query.filter(self.model.price == price)
        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        result = [self.schema.model_validate(model) for model in result.scalars().all()]
        return result
        
