class MyAppException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
class RoomNotAvailableException(MyAppException):
    detail = "Номер недоступен для бронирования"

