
from src.exceptions.base import MyAppException, MyAppHTTPException


class FacilityAlreadyExistsException(MyAppException):
    detail = "Такое удобство уже существует"


class FacilityAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Такое удобство уже существует"
