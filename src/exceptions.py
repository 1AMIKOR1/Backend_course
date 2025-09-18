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


class ObjectAlreadyExistsException(MyAppException):
    detail = "Похожий объект уже существует"


class MyAppHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Номера не существует"


class HotelNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Отеля не существует"
