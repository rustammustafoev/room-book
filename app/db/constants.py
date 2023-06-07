from enum import Enum


class RoomType(str, Enum):
    FOCUS = 'focus'
    TEAM = 'team'
    CONFERENCE = 'conference'
