from src.schemas.facilities import SFacilityAdd


async def test_add_facilities(ac):
    new_facility = SFacilityAdd(title="WI-FI")
    response = await ac.post(url="/facilities/", json=new_facility.model_dump())
    facility = response.json()["data"]
    assert isinstance(facility, dict)
    assert facility["title"] == new_facility.title
    assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get(url="/facilities/")
    isinstance(response.json(), list)
    assert response.status_code == 200
