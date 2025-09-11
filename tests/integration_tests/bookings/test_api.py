import pytest
from src.schemas.bookings import SBoookingAddRequest

parameters = "room_id, date_from, date_to, status_code"
values = [
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 409),
    (1, "2025-09-01", "2025-09-10", 409),
]


@pytest.mark.parametrize(parameters, values)
async def test_add_bookings(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):

    booking = SBoookingAddRequest(room_id=room_id, date_from=date_from, date_to=date_to)

    response = await authenticated_ac.post(
        url="/bookings/", json=booking.model_dump(mode="json")
    )
    assert response.status_code == status_code
    if status_code == 200:
        new_booking = response.json()["data"]
        assert isinstance(new_booking, dict)
        assert new_booking["room_id"] == booking.room_id
