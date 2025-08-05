from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.facilities import SFacilityGet, SFacilityAdd, SFacilityPatch

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("/", summary="Получение списка удобств")
async def get_facilities(
    db: DBDep
)-> list[SFacilityGet] | None:
    return await db.facilities.get_filtered()

@router.post("/", summary="Добавление нового удобства")
async def add_facility(
    db: DBDep,
    facility: SFacilityAdd = Body(openapi_example="холодильник")
)-> dict | None:
    data: None | SFacilityGet = await db.facilities.add(facility)
    await db.commit()
    return {"status": "OK", "data": data}