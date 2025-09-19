import pytest

parameters_test_get_rooms = "hotel_id, date_from, date_to, status_code"
values_test_get_rooms = [
    (2, "2025-07-25", "2025-07-30", 200),
    (2, "2025-07-25", "2025-07-20", 400),
    (99876, "2025-07-25", "2025-07-30", 404),
]


@pytest.mark.parametrize(parameters_test_get_rooms, values_test_get_rooms)
async def test_get_rooms(hotel_id, date_from, date_to, status_code, ac):
    params = {"date_from": date_from, "date_to": date_to}
    response = await ac.get(url=f"/hotels/{hotel_id}/rooms", params=params)
    # print(f"{response.json()=}")
    assert response.status_code == status_code


parameters_test_add_room = (
    "hotel_id",
    "title",
    "description",
    "price",
    "quantity",
    "status_code",
)
values_test_add_room = [
    (1, "эконом 2-х", "двухместный номер", 2000, 5, 200),
    (1, "люкс 2-х", "двухместный номер", 5000, 5, 200),
    (2970, "эконом 2-х", "двухместный номер", 2000, 5, 404),
]


@pytest.mark.parametrize(parameters_test_add_room, values_test_add_room)
async def test_add_room(hotel_id, title, description, price, quantity, status_code, ac):
    json_request = {
        "title": title,
        "description": description,
        "price": price,
        "quantity": quantity,
    }
    response = await ac.post(url=f"/hotels/{hotel_id}/rooms", json=json_request)
    # print(f"{response.json()=}")
    assert response.status_code == status_code


parameters_test_get_room = (
    "hotel_id",
    "room_id",
    "status_code",
)
values_test_get_room = [
    (1, 5, 200),
    (1, 6, 200),
    (2970, 5, 404),
]


@pytest.mark.parametrize(parameters_test_get_room, values_test_get_room)
async def test_get_room(hotel_id, room_id, status_code, ac):

    response = await ac.get(url=f"/hotels/{hotel_id}/rooms/{room_id}")
    # print(f"{response.json()=}")
    room = response.json()
    if response.status_code == 200:
        assert room["id"] == room_id
    assert response.status_code == status_code


parameters_test_edit_room = (
    "hotel_id",
    "room_id",
    "title",
    "description",
    "price",
    "quantity",
    "status_code",
)
values_test_edit_room = [
    (1, 5, "эконом 3-х", "трехместный номер", 3000, 4, 200),
    (1, 6, "люкс 3-х", "трехместный номер", 10000, 7, 200),
    (1, 24324, "люкс 3-х", "трехместный номер", 10000, 7, 404),
    (2970, 2, "эконом 3-х", "трехместный номер", 3000, 4, 404),
]


@pytest.mark.parametrize(parameters_test_edit_room, values_test_edit_room)
async def test_edit_room(
    hotel_id, room_id, title, description, price, quantity, status_code, ac
):
    json_request = {
        "title": title,
        "description": description,
        "price": price,
        "quantity": quantity,
    }
    response = await ac.put(
        url=f"/hotels/{hotel_id}/rooms/{room_id}", json=json_request
    )
    print(f"{response.json()=}")
    assert response.status_code == status_code


parameters_test_part_edit_room = (
    "hotel_id",
    "room_id",
    "title",
    "description",
    "price",
    "quantity",
    "status_code",
)
values_test_part_edit_room = [
    (1, 5, "эконом 3-х", None, 3000, 0, 200),
    (1, 6, "Люкс", None, 1000, 8, 200),
    (1, 24324, "люкс 3-х", "трехместный номер", 10000, 7, 404),
    (2970, 2, "эконом 3-х", "трехместный номер", 3000, 4, 404),
]


@pytest.mark.parametrize(parameters_test_part_edit_room, values_test_part_edit_room)
async def test_part_edit_room(
    hotel_id, room_id, title, description, price, quantity, status_code, ac
):
    json_request = {
        "title": title,
        "description": description,
        "price": price,
        "quantity": quantity,
    }
    response = await ac.patch(
        url=f"/hotels/{hotel_id}/rooms/{room_id}", json=json_request
    )
    print(f"{response.json()=}")
    assert response.status_code == status_code


parameters_test_delete_room = (
    "hotel_id",
    "room_id",
    "status_code",
)
values_test_delete_room = [
    (1, 3, 404),
    (1, 4, 404),
    (1, 24324, 404),
    (2970, 3, 404),
    (1, 5, 200),
    (1, 6, 200),
]


@pytest.mark.parametrize(parameters_test_delete_room, values_test_delete_room)
async def test_delete_room(hotel_id, room_id, status_code, ac):
    response = await ac.delete(url=f"/hotels/{hotel_id}/rooms/{room_id}")
    # print(f"{response.json()=}")
    assert response.status_code == status_code
