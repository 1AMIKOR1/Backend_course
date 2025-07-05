from pydantic import BaseModel


class SHotel(BaseModel):
    title: str
    location: str

class SHotelGet(BaseModel):
    id: int | None = None
    title: str | None = None
    location: str | None = None

class SHotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None