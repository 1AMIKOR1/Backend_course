from src.exceptions.base import MyAppException, MyAppHTTPException


class HotelNotFoundException(MyAppException):
    detail = "Отель не найден"


class HotelNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Отеля не существует"
