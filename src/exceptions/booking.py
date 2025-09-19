from src.exceptions.base import MyAppException, MyAppHTTPException


class RoomNotAvailableException(MyAppException):
    detail = "Номер недоступен для бронирования"


class RoomNotAvailableHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Номер недоступен для бронирования"
