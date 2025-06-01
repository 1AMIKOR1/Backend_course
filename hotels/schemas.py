from pydantic import BaseModel,Field


class SHotel(BaseModel):
    title: str
    count_of_stars: int

class SHotelGet(BaseModel):
    id: int | None = None
    title: str | None = None
    count_of_stars: int | None = None
    page : int | None = Field(0)
    perpage : int | None = Field(5)

class SHotelPatch(BaseModel):
    title: str | None = None
    count_of_stars: int | None = None