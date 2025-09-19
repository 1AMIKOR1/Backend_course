from src.schemas.facilities import SFacilityAdd, SFacilityGet
from src.services.base import BaseService
from src.tasks.celery_tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        facilities = await self.db.facilities.get_filtered()
        return facilities

    async def create_facility(self, facility_data: SFacilityAdd):
        facility: None | SFacilityGet = await self.db.facilities.add(facility_data)
        await self.db.commit()
        test_task.delay()
        # type: ignore
        return facility
