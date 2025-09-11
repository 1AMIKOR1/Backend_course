import pytest
from src.schemas.bookings import SBookingAddRequest

parameters_test_add_bookings = "room_id, date_from, date_to, status_code"
values_test_add_bookings = [
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 200),
    (1, "2025-09-01", "2025-09-10", 409),
]


@pytest.mark.parametrize(parameters_test_add_bookings, values_test_add_bookings)
async def test_add_bookings(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):

    booking = SBookingAddRequest(room_id=room_id, date_from=date_from, date_to=date_to)

    response = await authenticated_ac.post(
        url="/bookings/", json=booking.model_dump(mode="json")
    )
    assert response.status_code == status_code
    if status_code == 200:
        new_booking = response.json()["data"]
        assert isinstance(new_booking, dict)
        assert new_booking["room_id"] == booking.room_id

parameters_test_add_get_my_bookings = (
    "room_id, date_from, date_to, status_code, count_of_booking"
)
values_test_add_get_my_bookings = [
    (1, "2025-09-01", "2025-09-10", 200, 1),
    (1, "2025-09-01", "2025-09-10", 200, 2),
    (1, "2025-09-01", "2025-09-10", 200, 3),
    (1, "2025-09-01", "2025-09-10", 200, 4),
    (1, "2025-09-01", "2025-09-10", 200, 5),
    (1, "2025-09-01", "2025-09-10", 409, 5),
]


@pytest.mark.parametrize(
    parameters_test_add_get_my_bookings, values_test_add_get_my_bookings
)
async def test_add_get_my_bookings(
    room_id,
    date_from,
    date_to,
    status_code,
    count_of_booking,
    db,
    authenticated_ac,
    delete_all_bookings,
):
    booking = SBookingAddRequest(room_id=room_id, date_from=date_from, date_to=date_to)

    response_add = await authenticated_ac.post(
        url="/bookings/", json=booking.model_dump(mode="json")
    )

    response_get = await authenticated_ac.get(url="/bookings/me")
    bookings = response_get.json()
    assert response_add.status_code == status_code
    assert response_get.status_code == 200

    assert count_of_booking == len(bookings)

    if response_add.status_code == 200:
        new_booking = response_add.json()["data"]
        assert isinstance(new_booking, dict)
        assert new_booking["room_id"] == booking.room_id
