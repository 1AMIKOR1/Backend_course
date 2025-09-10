from datetime import date
from fastapi import APIRouter, Body, Query

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import SHotelAdd, SHotelGet, SHotelPatch


add_hotel_examples = {
    "normal": {
        "summary": "Сочи",
        "description": "Пример нормального объекта.",
        "value": {
            "title": "Sochi Beach Resort",
            "location": "г. Сочи, ул. Ленина, д. 35",
        },
    },
    "invalid": {
        "summary": "Novosibirsk",
        "description": "Пример неправильного объекта.",
        "value": {"title": "Novosibirsk Comfort Stay"},
    },
}


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получение списка отелей", response_model=list[SHotelGet])
# @cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(example="2025-07-25", description="Дата заезда"),
    date_to: date = Query(example="2025-07-30", description="Дата выезда"),
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    return await db.hotels.get_filtered_free_hotels(
        date_from=date_from,
        date_to=date_to,
        limit=pagination.per_page,
        offset=(pagination.per_page * (pagination.page - 1)),
        title=title,
        location=location,
    )


@router.get("/{hotel_id}", summary="Получение отеля по id", response_model=SHotelGet)
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("/", summary="Добавление нового отеля")
async def create_hotels(
    db: DBDep, hotel_data: SHotelAdd = Body(openapi_examples=add_hotel_examples)
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(db: DBDep, hotel_id: int) -> dict[str, str]:
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновление отеля по id")
async def update_hotel(
    db: DBDep, hotel_id: int, hotel_data: SHotelAdd
) -> dict[str, str]:
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля по id")
async def modify_hotel(
    db: DBDep, hotel_id: int, hotel_data: SHotelPatch
) -> dict[str, str]:

    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}
