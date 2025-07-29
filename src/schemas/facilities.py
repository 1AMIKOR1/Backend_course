from pydantic import BaseModel, ConfigDict


class SFacilityAdd(BaseModel):
    title: str


class SFacilityGet(SFacilityAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SFacilityPatch(BaseModel):
    title: str | None = None