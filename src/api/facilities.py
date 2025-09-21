from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions.facilities import FacilityAlreadyExistsException, FacilityAlreadyExistsHTTPException
from src.schemas.facilities import SFacilityGet, SFacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/", summary="Получение списка удобств")
@cache(expire=10)
async def get_facilities(db: DBDep) -> list[SFacilityGet] | None:
    # print("Иду в БД.")
    facilities = await FacilityService(db).get_facilities()

    return facilities


@router.post("/", summary="Добавление нового удобства")
async def add_facility(
    db: DBDep, facility_data: SFacilityAdd = Body(openapi_example="холодильник")
) -> dict | None:
    try:
        facility = await FacilityService(db).create_facility(facility_data)
    except FacilityAlreadyExistsException as ex:
        raise FacilityAlreadyExistsHTTPException from ex
    return {"status": "OK", "data": facility}
