import pytest

parameters_test_get_hotels = "date_from, date_to, status_code"
values_test_get_hotels = [
    ("2025-07-25", "2025-07-30", 200),
    ("2025-07-25", "2025-07-20", 400),
]


@pytest.mark.parametrize(parameters_test_get_hotels, values_test_get_hotels)
async def test_get_hotels(date_from, date_to, status_code, ac):
    params = {"date_from": date_from, "date_to": date_to}
    response = await ac.get(url="/hotels/", params=params)
    assert response.status_code == status_code
