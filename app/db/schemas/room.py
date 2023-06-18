from datetime import datetime

from pydantic import BaseModel

from app.db import constants


class RoomBase(BaseModel):
    name: str
    capacity: int
    type: constants.RoomType
    opens_at: datetime
    closes_at: datetime


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int

    class Config:
        orm_mode = True
