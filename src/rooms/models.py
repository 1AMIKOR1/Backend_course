from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.database import BaseModel


class RoomsModel(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]