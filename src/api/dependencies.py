from typing import Annotated
from fastapi import Depends, Request, HTTPException
from pydantic import BaseModel, Field
from src.database import async_session_maker

from src.services.auth import AuthService
from src.utils.db_manader import DBManager


class PaginationParams(BaseModel):
    page: int | None = Field(1, ge=1)
    per_page: int | None = Field(5, ge=1, le=30)


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
