from pydantic import BaseModel
from src.database import Base

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.schemas.facilities import SRoomFacilityAdd, SRoomFacility, SFacilityGet


class FacilitiesRepository(BaseRepository):
    model: Base = FacilitiesModel
    schema: BaseModel = SFacilityGet


class RoomsFacilitiesRepository(BaseRepository):
    model: Base = RoomsFacilitiesModel
    schema: BaseModel = SRoomFacility

    async def edit(
        self, room_id: int, new_facilities_ids: list[int] | None
    ):
        current_facilities_query = await self.get_all(room_id=room_id)

        current_facilities = set([
            room_facility.facility_id 
            for room_facility in current_facilities_query
        ])

        new_facilities = set(new_facilities_ids) if new_facilities_ids else set()
        to_delete = current_facilities - new_facilities
        to_add = new_facilities - current_facilities
        if to_delete:
            await self.delete(
                RoomsFacilitiesModel.room_id == room_id,
                RoomsFacilitiesModel.facility_id.in_(to_delete))
        if to_add:
            rooms_facilities_data = [
                SRoomFacilityAdd(room_id=room_id, facility_id=f_id)
                for f_id in to_add
            ]
            if rooms_facilities_data:
                await self.add_bulk(rooms_facilities_data)