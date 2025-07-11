from repositories.base import BaseRepository
from models.users import UsersModel
from schemas.users import SUser

class UsersRepository(BaseRepository):
    model = UsersModel
    schema = SUser