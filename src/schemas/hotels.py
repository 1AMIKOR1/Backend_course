from pydantic import BaseModel


class SHotelAdd(BaseModel):
    title: str
    location: str


class SHotelGet(SHotelAdd):
    id: int
    # model_config = ConfigDict(from_attributes=True)


class SHotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
