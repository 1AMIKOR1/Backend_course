from datetime import date
from src.schemas.bookings import SBoookingAdd, SBookingPatch, SBookingGet


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    price = 1000
    date_from = date(year=2025, month=9, day=1)
    date_to = date(year=2025, month=9, day=10)

    booking_data = SBoookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        price=price,
    )
    new_booking: SBookingGet = await db.bookings.add(booking_data)

    finded_booking: SBookingGet = await db.bookings.get_one_or_none(id=new_booking.id)

    assert finded_booking

    assert new_booking == finded_booking

    updated_date_from = date(year=2026, month=9, day=1)
    updated_date_to = date(year=2026, month=9, day=1)

    edit_booking_data = SBookingPatch(
        date_from=updated_date_from,
        date_to=updated_date_to,
    )
    await db.bookings.edit(
        data=edit_booking_data, exclude_unset=True, id=finded_booking.id
    )
    updated_booking: SBookingGet = await db.bookings.get_one_or_none(
        id=finded_booking.id
    )
    assert updated_booking
    assert updated_booking.id == finded_booking.id
    assert updated_booking.date_from == updated_date_from
    assert updated_booking.date_to == updated_date_to

    await db.bookings.delete(id=finded_booking.id)

    await db.commit()
