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
    new_booking = await db.bookings.add(booking_data)

    finded_booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert new_booking == finded_booking

    edit_boking_data = SBookingPatch(
        date_from=date(year=2026, month=9, day=1),
        date_to=date(year=2026, month=9, day=1),
    )
    await db.bookings.edit(
        data=edit_boking_data, exclude_unset=True, id=finded_booking.id
    )

    await db.bookings.delete(id=finded_booking.id)

    await db.commit()
