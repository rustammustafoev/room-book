from typing import Callable, Union, List
from datetime import date, time

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
        logger.info('Application is shutting down!')

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


def is_valid_date(date_: Union[date, None]) -> date:
    current_date = date.today()

    if date_ is None:
        date_ = current_date

    elif not (date_ >= current_date):
        raise HTTPException(status_code=400,
                            detail={'error': 'Specified date must not be in the past!'})

    return date_


def time_from_offset_aware_to_naive(value: time):
    return value.replace(tzinfo=None)


def get_available_time_slots(
        room_opens_at: time,
        room_closes_at: time,
        bookings: List[models.Booking],
):
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
    # TODO: Write unit tests for this
    for booking in bookings:
        booking_start_time = time_from_offset_aware_to_naive(booking.start_time)
        booking_end_time = time_from_offset_aware_to_naive(booking.end_time)
        if (
            (booking_start_time < start < booking_end_time)
            or (booking_start_time < end < booking_end_time)
            or (start < booking_start_time < end)
        ):
            return True

    return False


