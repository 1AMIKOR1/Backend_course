from src.schemas.facilities import SFacilityAdd


async def test_add_facilities(ac):
    new_facility = SFacilityAdd(title="WI-FI")
    response = await ac.post(url="/facilities/", json=new_facility.model_dump())
    facility = response.json()["data"]
    print(f"{facility=}")

    assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get(url="/facilities/")
    print(f"{response.json()=}")

    assert response.status_code == 200
