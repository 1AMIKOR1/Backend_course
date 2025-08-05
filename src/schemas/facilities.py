from pydantic import BaseModel, ConfigDict


class SFacilityAdd(BaseModel):
    title: str


class SFacilityGet(SFacilityAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SFacilityPatch(BaseModel):
    title: str | None = None


class SRoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class SRoomFacility(SRoomFacilityAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
   
