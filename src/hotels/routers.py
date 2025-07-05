from typing import Annotated
from fastapi import APIRouter, Body, Depends, Query
from src.hotels.models import HotelsModel
from src.hotels.dependencies import PaginationDep
from src.hotels.schemas import SHotel, SHotelGet, SHotelPatch
from src.database import async_session_maker, engine
from sqlalchemy import insert, select


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
    id: int | None = Query(None, description="Номер отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsModel)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.post("/", summary="Добавление нового отеля")
async def create_hotels(hotel_data: SHotel = Body(openapi_examples=add_hotel_examples)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.put("/hotels/{hotel_id}", summary="Обновление отеля по id")
def update_hotel(hotel_id: int, hotel_data: SHotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]

    hotel["title"] = hotel_data.title
    hotel["count_of_stars"] = hotel_data.count_of_stars

    return {"status": "OK"}


@router.patch("/hotels/{hotel_id}", summary="Частичное обновление отеля по id")
def modify_hotel(hotel_id: int, hotel_data: SHotelPatch):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]

    if hotel_data.count_of_stars or hotel_data.count_of_stars == 0:
        hotel["count_of_stars"] = hotel_data.count_of_stars
    if hotel_data.title:
        hotel["title"] = hotel_data.title

    return {"status": "OK"}
