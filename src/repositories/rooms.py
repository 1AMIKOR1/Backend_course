from datetime import date
from pydantic import BaseModel
from database import Base

from repositories.base import BaseRepository
from models.rooms import RoomsModel
from repositories.utils import rooms_ids_free
from schemas.rooms import SRoomGet


class RoomsRepository(BaseRepository):
    model: Base = RoomsModel
    schema: BaseModel = SRoomGet

    async def get_filtered_free_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
        price_from: int,
        price_to: int,
        title: str,
        limit: int,
        offset: int,
    ):

        rooms_ids_to_get = rooms_ids_free(
            hotel_id=hotel_id, 
            date_from=date_from, 
            date_to=date_to, 
            price_from=price_from, 
            price_to=price_to, 
            title=title
        )
        return await self.get_filtered(
            limit, 
            offset, 
            self.model.id.in_(rooms_ids_to_get)
        )
