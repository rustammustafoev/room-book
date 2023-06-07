from pydantic import BaseModel

from app.db import constants


class RoomBase(BaseModel):
    name: str
    capacity: int
    type: constants.RoomType


class RoomIn(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int

    class Config:
        orm_mode = True
