from unittest import expectedFailure
from fastapi import APIRouter, Body
from passlib.context import CryptContext

from src.repositories.users import UserAlreadyExists, UsersRepository
from src.schemas.users import SUserAdd, SUserRequestAdd
from src.database import async_session_maker

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


@router.post("/register",summary="Регистрация нового пользователя")
async def register_user(
    data: SUserRequestAdd = Body(openapi_examples=reg_user_examples),
) -> dict[str, str]:
    hashed_password = pwd_context.hash(data.password)
    new_user_data = SUserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}

        except UserAlreadyExists as e:
            await session.rollback()
            raise e
            


    
