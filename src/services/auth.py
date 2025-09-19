from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions.auth import (
    InvalidJWTTokenException,
    UserNotFoundException,
    InvalidPasswordException,
)
from src.schemas.users import SUserRequestAdd, SUserAdd, SUser
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password) -> str:
        return self.pwd_context.hash(plain_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, [settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError as ex:
            raise InvalidJWTTokenException from ex

    async def register_user(self, data: SUserRequestAdd):
        hashed_password: str = AuthService().hash_password(data.password)
        new_user_data = SUserAdd(email=data.email, hashed_password=hashed_password)
        await self.db.users.add(new_user_data)
        await self.db.commit()

    async def login_user(self, user_data: SUserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise UserNotFoundException
        if not self.verify_password(user_data.password, user.hashed_password):
            raise InvalidPasswordException

        access_token: str = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_me(self, user_id: int):
        return await self.get_user_with_check(user_id)

    async def get_user_with_check(self, user_id):
        user: None | SUser = await self.db.users.get_one_or_none(id=user_id)
        if not user:
            raise UserNotFoundException
        return user
