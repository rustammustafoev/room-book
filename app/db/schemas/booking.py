from datetime import datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    room: int
    resident: int
    start_time: datetime
    end_time: datetime


class BookingIn(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
