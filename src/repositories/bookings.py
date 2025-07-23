from pydantic import BaseModel
from database import Base
from models.bookings import BookingsModel
from repositories.base import BaseRepository
from schemas.bookings import SBookingGet


class BookingsRepository(BaseRepository):
    model: Base = BookingsModel
    schema: BaseModel = SBookingGet