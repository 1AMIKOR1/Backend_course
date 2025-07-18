from pydantic import BaseModel
from sqlalchemy import func, select
from database import Base
from repositories.base import BaseRepository
from models.rooms import RoomsModel
from schemas.rooms import SRoomGet


class RoomsRepository(BaseRepository):
    model: Base = RoomsModel
    schema: BaseModel = SRoomGet

    async def get_all(self, price, title, limit, offset):
        query = select(self.model)
        if price:
            query = query.filter(
                self.model.price == price
            )
        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return result.scalars().all()