from src.models.bookings import BookingsModel
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.models.users import UsersModel
from src.repositories.mapper.base import DataMapper
from src.schemas.bookings import SBookingGet
from src.schemas.facilities import SFacilityGet, SRoomFacility
from src.schemas.hotels import SHotelGet
from src.schemas.rooms import SRoomGet, SRoomWithRels
from src.schemas.users import SUser, SUserWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = SHotelGet


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = SRoomGet


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsModel
    schema = SRoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersModel
    schema = SUser


class UserDataWithHashedPassword(DataMapper):
    db_model = UsersModel
    schema = SUserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsModel
    schema = SBookingGet


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesModel
    schema = SFacilityGet


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesModel
    schema = SRoomFacility
