async def test_get_hotels(ac):

    date_from = "2025-09-25"
    date_to = "2025-09-30"

    params = {"date_from": date_from, "date_to": date_to}
    response = await ac.get(url="/hotels/", params=params)

    print(f"{response.json()=}")

    assert response.status_code == 200
