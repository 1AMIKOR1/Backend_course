from fastapi import APIRouter, Body, HTTPException, Query
from api.dependencies import DBDep, PaginationDep, UserIdDep
from schemas.bookings import SBookingGet, SBoookingAdd, SBoookingAddRequest  


router = APIRouter(prefix="/bookings", tags=["Бронирование"])

bookings_examples = {
    "normal": {
        "summary": "На неделю",
        "description": "Пример нормального объекта.",
        "value": {
            "room_id": 2,
            "date_from": "2025-07-20",
            "date_to": "2025-07-27"
        },
    },
    "invalid": {
        "summary": "Эконом",
        "description": "Пример неправильного объекта.",
        "value": {
        },
    },
}



@router.post("/",summary="Бронирование номера")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: SBoookingAddRequest = Body(openapi_examples=bookings_examples),
    
):
    room = (await db.rooms.get_one_or_none(id=booking_data.room_id))
    if room is  None:
        raise HTTPException(404, "Номера с таким id не существует!")
    else:
        price = room.price
    
    _booking_data = SBoookingAdd(
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
        )
    booking: None | SBookingGet = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}