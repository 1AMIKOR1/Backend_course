from fastapi import APIRouter, Body, Query
from api.dependencies import PaginationDep
from repositories.rooms import RoomsRepository
from schemas.rooms import SRoomAdd, SRoomGet, SRoomPatch
from src.database import async_session_maker

rooms_examples = {
    "normal": {
        "summary": "Люкс",
        "description": "Пример нормального объекта.",
        "value": {
            "hotel_id": 2,
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
            "hotel_id": "1",
            "title": "Супер Эконом",
            "description": "Обычный номер с минимальным набором удобств",
            "price": "10000",
            "quantity": "3",
        },
    },
}


router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/", summary="Получение списка номеров")
async def get_rooms(
    pagination: PaginationDep,
    price: int | None = Query(None, description="Стоимость номера"),
    title: str | None = Query(None, description="Название номера"),
) -> list[SRoomGet] | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            price=price,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )


@router.get("/{room_id}", summary="Получение номера по id")
async def get_room(room_id: int) -> SRoomGet | None:
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/", summary="Добавление нового номера")
async def create_hotels(room_data: SRoomAdd = Body(openapi_examples=rooms_examples)):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/{room_id}", summary="Удаление номера по id")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{room_id}", summary="Обновление номера по id")
async def update_hotel(room_id: int, room_data: SRoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление номера по id")
async def modify_hotel(room_id: int, room_data: SRoomPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            data=room_data, exclude_unset=True, id=room_id
        )
        await session.commit()

    return {"status": "OK"}
