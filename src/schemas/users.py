from pydantic import BaseModel, ConfigDict, EmailStr


class SUserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class SUserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class SUser(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class SUserWithHashedPassword(SUser):
    hashed_password: str
