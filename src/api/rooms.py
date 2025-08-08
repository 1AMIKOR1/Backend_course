from datetime import date
from fastapi import APIRouter, Body, Query
from src.schemas.facilities import SRoomFacilityAdd
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.rooms import (
    SRoomAdd,
    SRoomAddRequest,
    SRoomGet,
    SRoomPatch,
    SRoomPatchRequest, SRoomWithRels,
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
            "facilities_ids": [1, 2, 3]
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
    price_from: int | None = Query( 0, description="Начало диапазона стоимости номера"),
    price_to: int | None = Query(None, description="Конец диапазона стоимости номера"),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomWithRels] | None:

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


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: SRoomAddRequest=Body(openapi_examples=rooms_examples),
):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    print(_room_data)
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
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера по id")
async def update_room(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    room_data: SRoomAddRequest=Body(openapi_examples=rooms_examples)
):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
    if room_data.facilities_ids is not None and room_data.facilities_ids != []:
        await db.rooms_facilities.edit(room_id, room_data.facilities_ids)
    
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера по id"
)
async def modify_room(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    room_data: SRoomPatchRequest=Body(openapi_examples=rooms_examples)
):
    _room_data = SRoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    if room_data.facilities_ids is not None and room_data.facilities_ids != []:
        await db.rooms_facilities.edit(room_id, room_data.facilities_ids)

    await db.rooms.edit(
        data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    await db.commit()

    return {"status": "OK"}
