from typing import Callable, Union, List, Dict
from datetime import datetime, time

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger

from app.core import tortoise_config
from app.db import models


def start_up_handler(app: FastAPI) -> Callable:
    async def start_up() -> None:
        init_db(app)

    return start_up


def shut_down_handler(app: FastAPI) -> Callable:
    async def shut_down() -> None:
        pass

    return shut_down


def init_db(app: FastAPI) -> None:
    try:
        register_tortoise(
            app,
            db_url=tortoise_config.db_url,
            generate_schemas=tortoise_config.generate_schemas,
            modules=tortoise_config.modules
        )
    except Exception as e:
        logger.error('Error initializing db -> %s' % e)
    else:
        logger.success('Db is initialized successfully')


def check_date_format(date: str) -> bool:

    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True

    except ValueError:
        return False


def is_valid_date(date: Union[str, None]) -> str:
    current_date = datetime.now().strftime('%Y-%m-%d')

    if date is None:
        date = current_date

    elif not check_date_format(date):
        raise HTTPException(status_code=400,
                            detail={'error': 'Date does not match format YYYY-MM-DD'})

    elif not (date >= current_date):
        raise HTTPException(status_code=400,
                            detail={'error': 'Specified date must not be in the past!'})

    return date


def get_available_time_slots(
        room_opens_at: datetime,
        room_closes_at: datetime,
        bookings: List[models.Booking],
) -> List[Dict[str, datetime]]:
    available_slots = []

    for booking in bookings:
        if booking.start_time > room_opens_at:
            end_time = booking.start_time
            available_slots.append({'start': room_opens_at, 'end': end_time})
        room_opens_at = booking.end_time

    if room_opens_at < room_closes_at:
        available_slots.append({'start': room_opens_at, 'end': room_closes_at})

    return available_slots


def check_booking_time_for_clash(
        start: time,
        end: time,
        bookings: List[models.Booking],
) -> bool:
    for booking in bookings:
        if (
          start <= booking.end_time
          and end >= booking.start_time
        ):
            return True

    return False


