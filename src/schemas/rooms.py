from pydantic import BaseModel, ConfigDict


class SRoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class SRoomAdd(SRoomAddRequest):
    hotel_id: int
    

class SRoomGet(SRoomAdd):
    id: int 
    model_config = ConfigDict(from_attributes=True)
    
class SRoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class SRoomPatch(SRoomPatchRequest):
    hotel_id: int | None = None