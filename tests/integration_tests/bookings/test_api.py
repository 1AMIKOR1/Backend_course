from datetime import date

from src.schemas.bookings import SBoookingAddRequest
from src.schemas.rooms import SRoomGet


async def test_add_bookings(db, authenticated_ac):
    date_from = date(2025, 9, 1)
    date_to = date(2025, 9, 10)
    room: SRoomGet = (await db.rooms.get_all())[0]

    booking = SBoookingAddRequest(room_id=room.id, date_from=date_from, date_to=date_to)

    for i in range(room.quantity):
        response = await authenticated_ac.post(
            url="/bookings/", json=booking.model_dump(mode="json")
        )
        assert response.status_code == 200
        new_booking = response.json()["data"]
        assert isinstance(new_booking, dict)
        assert new_booking["room_id"] == booking.room_id
    response = await authenticated_ac.post(
        url="/bookings/", json=booking.model_dump(mode="json")
    )
    assert response.status_code == 409
