from datetime import datetime

from pydantic import BaseModel, EmailStr


class ResidentBase(BaseModel):
    name: str
    email: EmailStr
    start_date: datetime
    end_date: datetime


class ResidentIn(ResidentBase):
    pass


class ResidentOut(ResidentBase):
    id: int

    class Config:
        orm_mode = True
