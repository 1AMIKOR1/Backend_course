from src.exceptions.facilities import FacilityAlreadyExistsException
from src.schemas.facilities import SFacilityAdd, SFacilityGet
from src.services.base import BaseService
from src.tasks.celery_tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        facilities = await self.db.facilities.get_filtered()
        return facilities

    async def create_facility(self, facility_data: SFacilityAdd):
        await self.check_existing_facility(facility_data.title)
        facility: None | SFacilityGet = await self.db.facilities.add(
            facility_data
        )
        await self.db.commit()
        test_task.delay()
        # type: ignore
        return facility
    async def check_existing_facility(self, title:str):
        facility= await self.db.facilities.get_one_or_none(title=title)
        if facility:
            raise FacilityAlreadyExistsException
        return None
        
    async def check_existing_facilities(self, facilities_ids: list[int]):
        existing_facility_ids = await self.get_facilities()
        existing_facility_ids = {f.id for f in existing_facility_ids}
        valid_facility_ids = [
            f_id for f_id in facilities_ids if f_id in existing_facility_ids
        ]
        if valid_facility_ids:
            return valid_facility_ids
            # rooms_facilities_data = [
            #     SRoomFacilityAdd(room_id=room.id, facility_id=f_id)
            #     for f_id in valid_facility_ids
            # ]
        if valid_facility_ids == []:
            return None

        return None
