from datetime import date
from sqlalchemy import select


from sqlalchemy.orm.strategy_options import selectinload


from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.repositories.utils import rooms_ids_free
from src.schemas.rooms import SRoomGet, SRoomWithRels


class RoomsRepository(BaseRepository):

    model: type[RoomsModel] = RoomsModel
    schema: type[SRoomGet] = SRoomGet


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
        query = (

            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        return [SRoomWithRels.model_validate(model) for model in result.scalars().all()]

