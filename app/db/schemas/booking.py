from datetime import datetime, date

from pydantic import BaseModel


class BookingBase(BaseModel):
    resident: str
    start_time: datetime
    end_time: datetime
    date: date


class BookingIn(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    room: int
    resident: int
