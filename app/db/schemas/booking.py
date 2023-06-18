from datetime import time, date

from pydantic import BaseModel, Field, validator

from app.core import utils


class BookingBase(BaseModel):
    resident: str = Field(..., title='Resident name')
    start_time: time
    end_time: time
    date: date


class BookingIn(BookingBase):

    @validator('date', pre=True)
    def set_date(cls, value):

        date_ = utils.is_valid_date(value)

        return date_


class BookingOut(BookingBase):
    id: int
    room: int
    resident: int
