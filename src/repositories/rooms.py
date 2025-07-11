from repositories.base import BaseRepository
from models.rooms import RoomsModel


class RoomsRepository(BaseRepository):
    model = RoomsModel