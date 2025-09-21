from datetime import date
import logging

from src.exceptions.rooms import RoomNotFoundException
from src.schemas.facilities import SRoomFacilityAdd
from src.schemas.rooms import (
    SRoomAddRequest,
    SRoomAdd,
    SRoomGet,
    SRoomPatchRequest,
    SRoomPatch,
    SRoomWithRels,
)
from src.services.base import BaseService
from src.services.facilities import FacilityService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_free_rooms(
        self,
        hotel_id: int,
        pagination,
        date_from: date,
        date_to: date,
        price_from: int | None = None,
        price_to: int | None = None,
        title: str | None = None,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        return await self.db.rooms.get_filtered_free_rooms(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
            price_from=price_from,
            price_to=price_to,
            title=title,
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )

    async def get_room(self, room_id: int, hotel_id: int):
        room = await self.get_room_with_check(
            room_id=room_id, hotel_id=hotel_id
        )
        return room

    async def create_room(self, hotel_id: int, room_data: SRoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        # print(_room_data)
        room: None | SRoomWithRels = await self.db.rooms.add(_room_data)
        if (
            room_data.facilities_ids is not None
            and room_data.facilities_ids != []
        ):

            valid_facility_ids = await FacilityService(
                self.db
            ).check_existing_facilities(room_data.facilities_ids)
            if valid_facility_ids:
                rooms_facilities_data = [
                    SRoomFacilityAdd(room_id=room.id, facility_id=f_id)
                    for f_id in valid_facility_ids
                ]
                await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def delete_room(self, room_id: int, hotel_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id, hotel_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: SRoomAddRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id, hotel_id)

        _room_data = SRoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        if (
            room_data.facilities_ids is not None
            and room_data.facilities_ids != []
        ):
            valid_facility_ids = await FacilityService(
                self.db
            ).check_existing_facilities(room_data.facilities_ids)
            if valid_facility_ids:
                await self.db.rooms_facilities.edit_facilities(
                    room_id, valid_facility_ids
                )
        await self.db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def edit_room_partially(
        self, hotel_id: int, room_id: int, room_data: SRoomPatchRequest
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id, hotel_id)

        _room_data = SRoomPatch(
            hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
        )
        await self.db.rooms.edit(
            data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if (
            room_data.facilities_ids is not None
            and room_data.facilities_ids != []
        ):
            valid_facility_ids = await FacilityService(
                self.db
            ).check_existing_facilities(room_data.facilities_ids)

            if valid_facility_ids:
                await self.db.rooms_facilities.edit_facilities(
                    room_id, valid_facility_ids
                )
        await self.db.commit()

    async def get_room_with_check(
        self, room_id: int, hotel_id: int | None = None
    ):
        if hotel_id:
            room = await self.db.rooms.get_one_or_none(
                id=room_id, hotel_id=hotel_id
            )
        else:
            room = await self.db.rooms.get_one_or_none(id=room_id)
        if not room:
            raise RoomNotFoundException
        return room
