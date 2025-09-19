from fastapi import APIRouter, Body, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions.auth import (
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    InvalidPasswordHTTPException,
    InvalidPasswordException,
)
from src.schemas.users import SUser, SUserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

reg_user_examples = {
    "normal": {
        "summary": "With password",
        "description": "Пример нормального объекта.",
        "value": {"email": "wfwf24@gmail.com", "password": "qwerty12345"},
    },
    "invalid": {
        "summary": "Without password",
        "description": "Пример неправильного объекта.",
        "value": {"email": "Novosibirsk Comfort Stay"},
    },
}


@router.post("/register", summary="Регистрация нового пользователя")
async def register_user(
    db: DBDep,
    data: SUserRequestAdd = Body(openapi_examples=reg_user_examples),
) -> dict[str, str]:
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    user_data: SUserRequestAdd = Body(openapi_examples=reg_user_examples),
) -> dict[str, str]:
    try:
        access_token: str = await AuthService(db).login_user(user_data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except InvalidPasswordException:
        raise InvalidPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="Получение текущего пользователя")
async def get_me(db: DBDep, user_id: UserIdDep) -> SUser | None:
    try:
        user: None | SUser = await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return user


@router.post("/logout", summary="Выход пользователя из системы")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"status": "OK"}
