from pydantic import BaseModel
from src.database import Base

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesModel
from src.schemas.facilities import SFacilityGet


class FacilityRepository(BaseRepository):
    model: Base = FacilitiesModel
    schema: BaseModel = SFacilityGet