from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from sqlalchemy import insert, select
from src.repositories.base import BaseRepository
from src.models.users import UsersModel
from src.repositories.mapper.base import DataMapper
from src.repositories.mapper.mappers import UserDataMapper, UserDataWithHashedPassword
from src.schemas.users import SUser, SUserWithHashedPassword

class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Пользователь с таким email уже существует")

class UsersRepository(BaseRepository):
    model = UsersModel
    mapper: DataMapper = UserDataMapper

    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model =  result.scalars().one_or_none()

            return self.mapper.map_to_schema(model)
        
        except IntegrityError as e:        
            raise UserAlreadyExists()
        
    async def get_user_with_hashed_password(self, email: EmailStr) -> SUserWithHashedPassword|None:
        query = select(self.model).filter_by(email=email)

        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        
        if model is None:
            return None
        return UserDataWithHashedPassword.map_to_schema(model)

