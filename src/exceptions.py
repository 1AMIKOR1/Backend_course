from fastapi import HTTPException


class MyAppException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
class RoomNotAvailableException(MyAppException):
    detail = "Номер недоступен для бронирования"

class UserAlreadyExistsException(MyAppException):
    detail = "Пользователь с таким email уже существует"

class InvalidDateRangeException(MyAppException):
    detail = "Дата заезда не может быть позже даты выезда"

class ObjectNotFoundException(MyAppException):
    detail = "Объект не найден"

class RoomNotFoundHTTPException(HTTPException):
    status_code = 404
    detail = "Номера не существует"
    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code,self.detail, *args, **kwargs)

class HotelNotFoundHTTPException(HTTPException):
    status_code = 404
    detail = "Отеля не существует"
    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code,self.detail, *args, **kwargs)