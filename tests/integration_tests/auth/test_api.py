import pytest

parameters_test_user_auth = "password, email, register_status, login_status"
values_test_user_auth = [
    (
        "ihoud7gyvuUTGC6",
        "yfyy@ccc.com",
        200,
        200,
    ),  # Успешная регистрация и авторизация
    (
        "ihoud7gyvuUTGC6",
        "yfyy@ccc.com",
        409,
        200,
    ),  # Попытка повторной регистрации
    ("wrong_password", "yfyy@ccc.com", 409, 401),  # Неверный пароль при логине
    (
        "any_password",
        "nonexistent@test.com",
        401,
        401,
    ),  # Несуществующий пользователь
    ("", "invalid-email", 422, 422),  # Невалидные данные
]


@pytest.mark.parametrize(parameters_test_user_auth, values_test_user_auth)
async def test_user_auth(
    password: str, email: str, register_status: str, login_status: int, ac
):
    # /register
    if register_status != 401:
        response_reg = await ac.post(
            "/auth/register", json={"email": email, "password": password}
        )
        assert response_reg.status_code == register_status
    # /login
    response_login = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response_login.status_code == login_status
    if login_status == 200:
        assert ac.cookies["access_token"]
        # /me
        response_me = await ac.get("/auth/me")
        assert response_me.status_code == 200
        user = response_me.json()
        assert user["email"] == email
        assert "id" in user
        assert "password" not in user
        assert "hashed_password" not in user
        # /logout
        response_logout = await ac.post("/auth/logout")
        assert response_logout.status_code == 200
        assert ac.cookies.get("access_token") is None
        # /me
        response_after_logout = await ac.get("/auth/me")
        assert response_after_logout.status_code == 401
