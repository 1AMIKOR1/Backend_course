from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.rooms import RoomsModel

class FacilitiesModel(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    rooms: Mapped[list["RoomsModel"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )

    rooms: Mapped[list["RoomsModel"]] = relationship(
        secondary="rooms_facilities", 
        back_populates="facilities",
    )



class RoomsFacilitiesModel(Base):
    __tablename__ = "rooms_facilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))