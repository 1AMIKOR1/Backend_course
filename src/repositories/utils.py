from datetime import date

from sqlalchemy import func, select

from src.exceptions.base import InvalidDateRangeException
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel


def rooms_ids_free(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
    price_from: int | None = None,
    price_to: int | None = None,
    title: str | None = None,
):
    if date_from > date_to:
        raise InvalidDateRangeException
    rooms_booked = (
        select(BookingsModel.room_id, func.count("*").label("booked_rooms"))
        .select_from(BookingsModel)
        .filter(
            BookingsModel.date_from <= date_to,
            BookingsModel.date_to >= date_from,
        )
        .group_by(BookingsModel.room_id)
        .cte(name="rooms_booked")
    )
    rooms_free = (
        select(
            RoomsModel.id.label("room_id"),
            (RoomsModel.quantity - func.coalesce(rooms_booked.c.booked_rooms, 0)).label(
                "free_rooms"
            ),
            RoomsModel.price,
            RoomsModel.title,
        )
        .select_from(RoomsModel)
        .outerjoin(rooms_booked, RoomsModel.id == rooms_booked.c.room_id)
        .cte(name="rooms_free")
    )
    rooms_ids_for_hotel = select(RoomsModel.id).select_from(RoomsModel)

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    if price_from is not None and price_to is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter(
            RoomsModel.price <= price_to, RoomsModel.price >= price_from
        )
    if title is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter(
            func.lower(RoomsModel.title).contains(title.strip().lower())
        )

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    rooms_ids_to_get = (
        select(rooms_free.c.room_id)
        .select_from(rooms_free)
        .filter(
            rooms_free.c.free_rooms > 0,
            rooms_free.c.room_id.in_(rooms_ids_for_hotel),
        )
    )
    return rooms_ids_to_get
