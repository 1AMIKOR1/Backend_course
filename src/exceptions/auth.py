from src.exceptions.base import MyAppException, MyAppHTTPException


class UserAlreadyExistsException(MyAppException):
    detail = "Пользователь с таким email уже существует"


class InvalidJWTTokenException(MyAppException):
    detail = "Неверный токен"


class InvalidPasswordException(MyAppException):
    detail = "Неверный пароль"


class UserNotFoundException(MyAppException):
    detail = "Пользователя не существует"


class InvalidTokenHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "Неверный токен доступа"


class UserAlreadyExistsHTTPException(MyAppHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserNotFoundHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "Пользователя не существует"


class InvalidPasswordHTTPException(MyAppHTTPException):
    status_code = 401
    detail = "Неверный пароль"
