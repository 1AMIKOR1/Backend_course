class RoomNotAvailableException(Exception):
    def __init__(self, room_id: int):
        self.room_id = room_id
        super().__init__(f"Room with id {room_id} is not available for booking")
