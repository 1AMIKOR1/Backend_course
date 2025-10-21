from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions.base import InvalidDateRangeException
from src.exceptions.hotels import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import SHotelAdd, SHotelGet, SHotelPatch
from src.services.hotels import HotelService

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
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(example="2025-07-25", description="Дата заезда"),
    date_to: date = Query(example="2025-07-30", description="Дата выезда"),
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    try:
        hotels = await HotelService(db).get_filtered_free_hotels(
            pagination, date_from, date_to, location, title
        )
    except InvalidDateRangeException as e:
        raise HTTPException(status_code=400, detail=e.detail)

    return hotels


@router.get("/{hotel_id}", summary="Получение отеля по id", response_model=SHotelGet)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return hotel


@router.post("/", summary="Добавление нового отеля")
async def create_hotels(
    db: DBDep, hotel_data: SHotelAdd = Body(openapi_examples=add_hotel_examples)
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(db: DBDep, hotel_id: int) -> dict[str, str]:
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.put("/{hotel_id}", summary="Обновление отеля по id")
async def update_hotel(
    db: DBDep, hotel_id: int, hotel_data: SHotelAdd
) -> dict[str, str]:
    try:
        await HotelService(db).edit_hotel(hotel_data=hotel_data, hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля по id")
async def modify_hotel(
    db: DBDep, hotel_id: int, hotel_data: SHotelPatch
) -> dict[str, str]:
    try:
        await HotelService(db).edit_hotel_partially(
        hotel_data=hotel_data, hotel_id=hotel_id
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
