from fastapi import APIRouter, Body, Query
from src.repositories.hotels import HotelsRepository
from src.hotels.dependencies import PaginationDep
from src.hotels.schemas import SHotel, SHotelGet, SHotelPatch
from src.database import async_session_maker

add_hotel_examples = {
    "normal": {
        "summary": "Сочи",
        "description": "Пример нормального объекта.",
        "value": {"title": "Sochi Beach Resort", "location": "г. Сочи"},
    },
    "invalid": {
        "summary": "Novosibirsk",
        "description": "Пример неправильного объекта.",
        "value": {"title": "Novosibirsk Comfort Stay"},
    },
}


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получение списка отелей")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("/", summary="Добавление нового отеля")
async def create_hotels(hotel_data: SHotel = Body(openapi_examples=add_hotel_examples)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновление отеля по id")
async def update_hotel(hotel_id: int, hotel_data: SHotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление отеля по id")
async def modify_hotel(hotel_id: int, hotel_data: SHotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            data=hotel_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()

    return {"status": "OK"}
