from datetime import date

from src.exceptions.hotels import HotelNotFoundException
from src.schemas.hotels import SHotelAdd, SHotelPatch
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_filtered_free_hotels(
        self,
        pagination,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
    ):
        hotels = await self.db.hotels.get_filtered_free_hotels(
            date_from=date_from,
            date_to=date_to,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
            title=title,
            location=location,
        )
        return hotels

    async def get_hotel(self, hotel_id: int):
        hotel = await self.get_hotel_with_check(hotel_id)
        return hotel

    async def add_hotel(self, hotel_data: SHotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):

        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def edit_hotel(self, hotel_data: SHotelAdd, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.edit(data=hotel_data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_data: SHotelPatch, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if not hotel:
            raise HotelNotFoundException
        return hotel
