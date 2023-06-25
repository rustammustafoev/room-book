from pydantic import BaseModel, Field


class BookingResident(BaseModel):
    name: str


class BookingBase(BaseModel):
    start: str
    end: str


class BookingIn(BookingBase):
    resident: BookingResident = Field(..., title='Resident name')


class BookingOut(BookingBase):
    id: int
    room_id: int
    resident_id: int
