from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from sqlalchemy import insert
from repositories.base import BaseRepository
from models.users import UsersModel
from schemas.users import SUser

class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Пользователь с таким email уже существует")

class UsersRepository(BaseRepository):
    model = UsersModel
    schema = SUser

    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            return result.scalars().one_or_none()
        
        except IntegrityError as e:        
            raise UserAlreadyExists()

