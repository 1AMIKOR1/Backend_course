import logging

from fastapi import APIRouter, Body, HTTPException, Query
from src.api.dependencies import DBDep, PaginationDep, UserIdDep
from src.schemas.bookings import SBookingGet, SBoookingAdd, SBoookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирование"])

bookings_examples = {
    "normal": {
        "summary": "На неделю",
        "description": "Пример нормального объекта.",
        "value": {"room_id": 2, "date_from": "2025-07-20", "date_to": "2025-07-27"},
    },
    "invalid": {
        "summary": "Эконом",
        "description": "Пример неправильного объекта.",
        "value": {},
    },
}


@router.get("/", summary="Просмотр всех бронирований")
async def get_bookings(
    db: DBDep, pagination: PaginationDep
) -> list[SBookingGet] | None:

    return await db.bookings.get_filtered(
        limit=pagination.per_page, offset=(pagination.per_page * (pagination.page - 1))
    )


@router.get("/me", summary="Просмотр бронирований текущего пользователя")
async def get_bookings_current_user(
    db: DBDep, user_id: UserIdDep, pagination: PaginationDep
) -> list[SBookingGet] | None:
    return await db.bookings.get_filtered(
        limit=pagination.per_page,
        offset=(pagination.per_page * (pagination.page - 1)),
        user_id=user_id,
    )


@router.post("/", summary="Бронирование номера")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: SBoookingAddRequest = Body(openapi_examples=bookings_examples),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(404, "Номера с таким id не существует!")
    else:
        price = room.price

    _booking_data = SBoookingAdd(
        user_id=user_id, price=price, **booking_data.model_dump()
    )
    booking: None | SBookingGet = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
