from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions.base import InvalidDateRangeException
from src.exceptions.hotels import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.exceptions.rooms import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import (
    SRoomAddRequest,
    SRoomPatchRequest,
    SRoomWithRels,
)
from src.services.rooms import RoomService

rooms_examples = {
    "normal": {
        "summary": "Люкс",
        "description": "Пример нормального объекта.",
        "value": {
            "title": "Супер Люкс",
            "description": "Супер кофротный номер со всеми удобствами",
            "price": 10000,
            "quantity": 3,
            "facilities_ids": [1, 2, 3],
        },
    },
}


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep,
    date_from: date = Query(example="2025-07-25", description="Дата заезда"),
    date_to: date = Query(example="2025-07-30", description="Дата выезда"),
    price_from: int | None = Query(
        0, description="Начало диапазона стоимости номера"
    ),
    price_to: int | None = Query(
        None, description="Конец диапазона стоимости номера"
    ),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomWithRels] | None:
    try:
        rooms = await RoomService(db).get_filtered_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
            price_from=price_from,
            price_to=price_to,
            title=title,
            pagination=pagination,
        )
    except InvalidDateRangeException as e:
        raise HTTPException(400, e.detail)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room = await RoomService(db).get_room(
            room_id=room_id, hotel_id=hotel_id
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return room


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples),
):
    try:
        room = await RoomService(db).create_room(
            hotel_id=hotel_id, room_data=room_data
        )
        return {"status": "OK", "data": room}
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(room_id, hotel_id)
        return {"status": "OK"}

    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex

    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера по id")
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples),
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера по id"
)
async def modify_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: SRoomPatchRequest = Body(openapi_examples=rooms_examples),
):
    try:
        await RoomService(db).edit_room_partially(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
