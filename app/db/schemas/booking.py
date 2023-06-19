from datetime import time, date

from pydantic import BaseModel, Field

from app.db.constants import BookingStatus


class BookingBase(BaseModel):
    date: date
    start_time: time
    end_time: time
    status: BookingStatus = Field(default=BookingStatus.RESERVED)


class BookingIn(BookingBase):
    resident: str = Field(..., title='Resident name')


class BookingOut(BookingBase):
    id: int
    room_id: int
    resident_id: int
