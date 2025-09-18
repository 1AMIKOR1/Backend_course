from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    InvalidDateRangeException,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.facilities import SRoomFacilityAdd
from src.schemas.rooms import (
    SRoomAdd,
    SRoomAddRequest,
    SRoomGet,
    SRoomPatch,
    SRoomPatchRequest,
    SRoomWithRels,
)

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
    price_from: int | None = Query(0, description="Начало диапазона стоимости номера"),
    price_to: int | None = Query(None, description="Конец диапазона стоимости номера"),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomWithRels] | None:
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundHTTPException
    try:
        return await db.rooms.get_filtered_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
            price_from=price_from,
            price_to=price_to,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )
    except InvalidDateRangeException as e:
        raise HTTPException(400, e.detail)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise RoomNotFoundHTTPException
    return room


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples),
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundHTTPException
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    # print(_room_data)
    room: None | SRoomGet = await db.rooms.add(_room_data)
    if room_data.facilities_ids is not None and room_data.facilities_ids != []:
        rooms_facilities_data: list[SRoomFacilityAdd] = [
            SRoomFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        if rooms_facilities_data:
            await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера по id")
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples),
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundHTTPException
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        if room_data.facilities_ids is not None and room_data.facilities_ids != []:
            await db.rooms_facilities.edit_facilities(room_id, room_data.facilities_ids)

        await db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера по id"
)
async def modify_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: SRoomPatchRequest = Body(openapi_examples=rooms_examples),
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundHTTPException
    _room_data = SRoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    try:
        await db.rooms.edit(
            data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if room_data.facilities_ids is not None and room_data.facilities_ids != []:
            await db.rooms_facilities.edit_facilities(room_id, room_data.facilities_ids)
        await db.commit()

        return {"status": "OK"}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
