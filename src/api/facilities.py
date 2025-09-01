import json

from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep, PaginationDep
from src.init import redis_manager
from src.schemas.facilities import SFacilityGet, SFacilityAdd, SFacilityPatch

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("/", summary="Получение списка удобств")
async def get_facilities(
    db: DBDep
)-> list[SFacilityGet] | None:
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"facilities_from_cache: {facilities_from_cache}")
    if not facilities_from_cache:
        print("Иду в БД.")
        facilities = await db.facilities.get_filtered()
        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts

@router.post("/", summary="Добавление нового удобства")
async def add_facility(
    db: DBDep,
    facility: SFacilityAdd = Body(openapi_example="холодильник")
)-> dict | None:
    data: None | SFacilityGet = await db.facilities.add(facility)
    await db.commit()
    return {"status": "OK", "data": data}