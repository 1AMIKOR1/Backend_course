from fastapi import APIRouter, Body, HTTPException, Response
from pydantic import BaseModel


from api.dependencies import UserIdDep
from services.auth import AuthService
from src.repositories.users import UserAlreadyExists, UsersRepository
from src.schemas.users import SUser, SUserAdd, SUserRequestAdd
from src.database import async_session_maker


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
    data: SUserRequestAdd = Body(openapi_examples=reg_user_examples),
) -> dict[str, str]:
    hashed_password:str = AuthService().hash_password(data.password)
    new_user_data = SUserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}

        except UserAlreadyExists as e:
            await session.rollback()
            raise e


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
    response: Response,
    data: SUserRequestAdd = Body(openapi_examples=reg_user_examples),
) -> dict[str, str]:
      async with async_session_maker() as session:

        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )

        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не существует"
            )

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token: str = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me",summary="Получение текущего пользователя")
async def get_me(user_id: UserIdDep) -> SUser:
    async with async_session_maker() as session:
        user: None | BaseModel = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
    
@router.post("/logout", summary="Выход пользователя из системы")
async def logout(response:Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"status": "OK"}
