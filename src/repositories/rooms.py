from repositories.base import BaseRepository
from rooms.models import RoomsModel


class RoomsRepository(BaseRepository):
    model = RoomsModel