from datetime import time

from pydantic import BaseModel

from app.db import constants


class RoomBase(BaseModel):
    name: str
    capacity: int
    type: constants.RoomType
    opens_at: time
    closes_at: time


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int

    class Config:
        orm_mode = True


RoomInExample = {
    'name': 'Resident',
    'capacity': 15,
    'type': 'focus',
    'opens_at': '9:00:00',
    'closes_at': '18:00:00'
}

RoomBookingExample = {
    "date": "2023-06-19",
    "start_time": "9:00:00",
    "end_time": "10:00:00",
    "status": "reserved",
    "resident": "Resident"
}
