from src.exceptions.base import MyAppHTTPException, MyAppException


class RoomNotFoundException(MyAppException):
    detail = "Номера не существует"


class RoomNotFoundHTTPException(MyAppHTTPException):
    status_code = 404
    detail = "Номера не существует"
