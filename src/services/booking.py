from src.schemas.bookings import SBookingAdd, SBookingAddRequest, SBookingGet
from src.services.auth import AuthService
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_filtered_booking(self, pagination):
        bookings = await self.db.bookings.get_filtered(
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
        )
        return bookings

    async def get_bookings_current_user(
        self, user_id: int, pagination
    ) -> list[SBookingGet]:
        await AuthService(self.db).get_user_with_check(user_id)
        booking = await self.db.bookings.get_filtered(
            limit=pagination.per_page,
            offset=(pagination.per_page * (pagination.page - 1)),
            user_id=user_id,
        )
        return booking

    async def create_booking(self, user_id: int, booking_data: SBookingAddRequest):
        room = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        price = room.price
        _booking_data = SBookingAdd(
            user_id=user_id, price=price, **booking_data.model_dump()
        )

        booking: SBookingGet = await self.db.bookings.add_booking(
            _booking_data, room.hotel_id
        )
        await self.db.commit()

        return booking
