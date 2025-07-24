from fastapi import APIRouter, Body, Query
from api.dependencies import DBDep, PaginationDep
from schemas.rooms import SRoomAdd, SRoomAddRequest, SRoomGet, SRoomPatch, SRoomPatchRequest

rooms_examples = {
    "normal": {
        "summary": "Люкс",
        "description": "Пример нормального объекта.",
        "value": {
            "title": "Супер Люкс",
            "description": "Супер кофротный номер со всеми удобствами",
            "price": 10000,
            "quantity": 3,
        },
    },
    "invalid": {
        "summary": "Эконом",
        "description": "Пример неправильного объекта.",
        "value": {
            "title": "Супер Эконом",
            "description": "Обычный номер с минимальным набором удобств",
            "price": "10000",
            "quantity": "3",
        },
    },
}


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение списка номеров")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    pagination: PaginationDep,
    price: int | None = Query(None, description="Стоимость номера"),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomGet] | None:
    return await db.rooms.get_all(
        hotel_id=hotel_id,
        price=price,
        title=title,
        limit=pagination.per_page,
        offset=(pagination.per_page * (pagination.page - 1))
    )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(
    db: DBDep,
    hotel_id: int, 
    room_id: int
) -> SRoomGet | None:
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(
    db: DBDep,
    hotel_id: int, 
    room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples)
):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(
    db: DBDep,
    hotel_id: int, 
    room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера по id")
async def update_room(
    db: DBDep,
    hotel_id: int, 
    room_id: int, 
    room_data: SRoomAddRequest
):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера по id")
async def modify_room(
    db: DBDep,
    hotel_id: int, 
    room_id: int, 
    room_data: SRoomPatchRequest
):
    _room_data = SRoomPatch(hotel_id=hotel_id,**room_data.model_dump(exclude_unset=True))

    await db.rooms.edit(
        data=_room_data, 
        exclude_unset=True, 
        id=room_id, 
        hotel_id=hotel_id
    )
    await db.commit()

    return {"status": "OK"}
