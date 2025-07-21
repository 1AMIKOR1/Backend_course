from fastapi import APIRouter, Body, Query
from api.dependencies import PaginationDep
from repositories.rooms import RoomsRepository
from schemas.rooms import SRoomAdd, SRoomAddRequest, SRoomGet, SRoomPatch, SRoomPatchRequest
from src.database import async_session_maker

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
    hotel_id: int,
    pagination: PaginationDep,
    price: int | None = Query(None, description="Стоимость номера"),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomGet] | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            price=price,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера по id")
async def get_room(hotel_id: int, room_id: int) -> SRoomGet | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(hotel_id: int, room_data: SRoomAddRequest = Body(openapi_examples=rooms_examples)):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера по id")
async def update_room(hotel_id: int, room_id: int, room_data: SRoomAddRequest):
    _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера по id")
async def modify_room(hotel_id: int, room_id: int, room_data: SRoomPatchRequest):
    _room_data = SRoomPatch(hotel_id=hotel_id,**room_data.model_dump(exclude_unset=True))
    print(_room_data.model_dump_json())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        await session.commit()

    return {"status": "OK"}
