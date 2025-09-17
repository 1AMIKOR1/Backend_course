from datetime import date
from sqlalchemy import func, select

from src.exceptions import InvalidDateRangeException
from src.models.rooms import RoomsModel
from src.repositories.mapper.base import DataMapper
from src.repositories.mapper.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_free
from src.schemas.hotels import SHotelGet
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = SHotelGet
    mapper: DataMapper = HotelDataMapper

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

        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]

    async def get_filtered_free_hotels(
        self,
        date_from: date,
        date_to: date,
        limit: int,
        offset: int,
        location: str,
        title: str,
    ):

        # if date_from > date_to:
        #     raise InvalidDateRangeException

        rooms_ids_to_get = rooms_ids_free(
            date_from=date_from,
            date_to=date_to,
        )

        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        if title is not None:
            title = func.lower(HotelsModel.title).contains(title.strip().lower())
        if location is not None:
            location = func.lower(HotelsModel.location).contains(
                location.strip().lower()
            )

        return await self.get_filtered(
            limit,
            offset,
            HotelsModel.id.in_(hotels_ids_to_get),
            location,
            title,
        )
