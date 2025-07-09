from sqlalchemy import func, select
from hotels.schemas import SHotelGet
from src.hotels.models import HotelsModel
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = SHotelGet

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsModel)
        if location:
            query = query.filter(
                func.lower(HotelsModel.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsModel.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return result.scalars().all()
