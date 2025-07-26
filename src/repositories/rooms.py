from datetime import date
from pydantic import BaseModel
from sqlalchemy import func, select
from database import Base
from models.bookings import BookingsModel
from repositories.base import BaseRepository
from models.rooms import RoomsModel
from schemas.rooms import SRoomGet
from src.database import engine


class RoomsRepository(BaseRepository):
    model: Base = RoomsModel
    schema: BaseModel = SRoomGet

    async def get_all(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
        price_from: int,
        price_to: int,
        title: str,
        limit: int,
        offset: int,
    ):
        rooms_booked = (
            select(BookingsModel.room_id, func.count("*").label("booked_rooms"))
            .select_from(BookingsModel)
            .filter(
                BookingsModel.date_from <= date_to,
                BookingsModel.date_to >= date_from,
            )
            .group_by(BookingsModel.room_id)
            .cte(name="rooms_booked")
        )
        rooms_free = (
            select(
                self.model.id.label("room_id"),
                (
                    self.model.quantity - func.coalesce(rooms_booked.c.booked_rooms, 0)
                ).label("free_rooms"),
                self.model.price,
                self.model.title,
            )
            .select_from(self.model)
            .outerjoin(rooms_booked, self.model.id == rooms_booked.c.room_id)
            # .filter(self.model.hotel_id == hotel_id)
            .cte(name="rooms_free")
        )
        rooms_ids_for_hotel = (
            select(self.model.id).select_from(self.model).filter_by(hotel_id=hotel_id)
        )
        if price_from is not None and price_to is not None:
            rooms_ids_for_hotel = rooms_ids_for_hotel.filter(
                self.model.price <= price_to, self.model.price >= price_from
            )
        if title is not None:
            rooms_ids_for_hotel = rooms_ids_for_hotel.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )

        rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")
        rooms_ids_to_get = (
            select(rooms_free.c.room_id)
            .select_from(rooms_free)
            .filter(
                rooms_free.c.free_rooms > 0,
                rooms_free.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        # print(
        #     rooms_ids_to_get.compile(
        #         bind=engine, compile_kwargs={"literal_binds": True}
        #     )
        # )
        return await self.get_filtered(
            limit,
            offset,
            self.model.id.in_(rooms_ids_to_get)

        )
