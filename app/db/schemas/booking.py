from datetime import time, date, datetime

from pydantic import BaseModel, Field, validator

from app.core import utils
from app.db.constants import BookingStatus


class BookingBase(BaseModel):
    resident: str = Field(..., title='Resident name')
    date: date
    start_time: time
    end_time: time
    status: BookingStatus = Field(default=BookingStatus.RESERVED)


class BookingIn(BookingBase):

    @validator('date', pre=True)
    def set_date(cls, value):
        wrap_to_date = datetime.strptime(value, '%Y-%m-%d')
        parsed_date = date(wrap_to_date.year, wrap_to_date.month, wrap_to_date.day)
        date_ = utils.is_valid_date(parsed_date)

        return date_


class BookingOut(BookingBase):
    id: int
    room_id: int
    resident_id: int
