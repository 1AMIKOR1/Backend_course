from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, PaginationDep, UserIdDep
from src.exceptions.auth import UserNotFoundException, UserNotFoundHTTPException
from src.exceptions.booking import (
    RoomNotAvailableException,
    RoomNotAvailableHTTPException,
)
from src.exceptions.rooms import RoomNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import SBookingGet, SBookingAddRequest
from src.services.booking import BookingService

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

    return await BookingService(db).get_filtered_booking(pagination)


@router.get("/me", summary="Просмотр бронирований текущего пользователя")
async def get_bookings_current_user(
    db: DBDep, user_id: UserIdDep, pagination: PaginationDep
) -> list[SBookingGet] | None:
    try:
        booking = await BookingService(db).get_bookings_current_user(
            user_id, pagination
        )
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return booking


@router.post("/", summary="Бронирование номера")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: SBookingAddRequest = Body(openapi_examples=bookings_examples),
):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    except RoomNotAvailableException:
        raise RoomNotAvailableHTTPException
    return {"status": "OK", "data": booking}
