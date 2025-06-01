from typing import Annotated
from fastapi import APIRouter, Depends
from hotels.schemas import SHotel, SHotelGet, SHotelPatch


hotels = [
    {'id': 1, 'title': 'Moscow Grand Hotel', 'count_of_stars': 5},
    {'id': 2, 'title': 'Saint Petersburg Palace', 'count_of_stars': 4},
    {'id': 3, 'title': 'Sochi Beach Resort', 'count_of_stars': 3},
    {'id': 4, 'title': 'Kazan Central Inn', 'count_of_stars': 4},
    {'id': 5, 'title': 'Novosibirsk Comfort Stay', 'count_of_stars': 3},
    {'id': 6, 'title': 'Yekaterinburg Luxury Suites', 'count_of_stars': 5},
    {'id': 7, 'title': 'Vladivostok Sea View', 'count_of_stars': 4},
    {'id': 8, 'title': 'Nizhny Novgorod Cozy Hotel', 'count_of_stars': 3},
    {'id': 9, 'title': 'Kaliningrad Riverside', 'count_of_stars': 4},
    {'id': 10, 'title': 'Samara Business Hotel', 'count_of_stars': 3}
]

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/",summary='Получение списка отелей')
def get_hotels(
        hotel_filter: Annotated[SHotelGet,Depends()]
):
    hotels_ = []
    offset = hotel_filter.page
    limit = hotel_filter.page  + hotel_filter.perpage  # type: ignore
    for hotel in hotels[offset:limit]:
        if hotel_filter.id and hotel["id"] != hotel_filter.id:
            continue
        if hotel_filter.title and hotel["title"] != hotel_filter.title:
            continue
        if hotel_filter.count_of_stars and hotel["count_of_stars"] != hotel_filter.count_of_stars:
            continue
        hotels_.append(hotel)
    return hotels_

@router.post("/", summary='Добавление нового отеля')
def create_hotels(hotel_data: SHotel

):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "count_of_stars": hotel_data.count_of_stars
    })
    return {"status": "OK"}

@router.delete("/{hotel_id}", summary='Удаление отеля по id')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.put("/hotels/{hotel_id}", summary='Обновление отеля по id')
def update_hotel(
    hotel_id: int,
    hotel_data: SHotel
    ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]

    hotel["title"] = hotel_data.title
    hotel["count_of_stars"] = hotel_data.count_of_stars

    return {"status": "OK"}

@router.patch("/hotels/{hotel_id}", summary='Частичное обновление отеля по id')
def modify_hotel(
    hotel_id: int,
    hotel_data: SHotelPatch
    ):

    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]

    if hotel_data.count_of_stars or hotel_data.count_of_stars == 0:
        hotel["count_of_stars"] = hotel_data.count_of_stars
    if hotel_data.title:
        hotel["title"] = hotel_data.title

    return {"status": "OK"}
