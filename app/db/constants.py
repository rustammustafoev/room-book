from enum import Enum


class RoomType(str, Enum):
    FOCUS = 'focus'
    TEAM = 'team'
    CONFERENCE = 'conference'


class BookingStatus(str, Enum):
    RESERVED = 'reserved'
    CHECKED_IN = 'checked_in'
    CHECKED_OUT = 'checked_out'
    CANCELLED = 'cancelled'
