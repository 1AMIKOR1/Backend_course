from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
<<<<<<< HEAD
=======

from typing import TYPE_CHECKING
>>>>>>> origin/detached

from src.database import Base


class RoomsModel(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesModel"]] = relationship(
<<<<<<< HEAD
        back_populates="rooms",
        secondary="rooms_facilities",
=======

        back_populates="rooms",
        secondary="rooms_facilities",

>>>>>>> origin/detached
    )
