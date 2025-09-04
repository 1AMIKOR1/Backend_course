from sqlalchemy import select


from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.mapper.base import DataMapper
from src.repositories.mapper.mappers import FacilityDataMapper
from src.schemas.facilities import SRoomFacilityAdd, SRoomFacility, SFacilityGet


class FacilitiesRepository(BaseRepository):
    model: FacilitiesModel = FacilitiesModel
    mapper: DataMapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model: RoomsFacilitiesModel = RoomsFacilitiesModel
    mapper: DataMapper = FacilityDataMapper

    async def edit(
        self,
        room_id: int,
        new_facilities_ids: list[int] | None
    ):
        current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(current_facilities_ids_query)
        current_facilities_ids = result.scalars.all()

        ids_to_delete = set(current_facilities_ids) - set(new_facilities_ids)
        ids_to_add = set(new_facilities_ids) - set(current_facilities_ids)
        if ids_to_delete:
            await self.delete(
                RoomsFacilitiesModel.room_id == room_id,
                RoomsFacilitiesModel.facility_id.in_(ids_to_delete))
        if ids_to_add:
            rooms_facilities_data = [
                SRoomFacilityAdd(room_id=room_id, facility_id=f_id)
                for f_id in ids_to_add
            ]
            if rooms_facilities_data:
                await self.add_bulk(rooms_facilities_data)