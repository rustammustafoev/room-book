from typing import Callable, Union, List
from datetime import date, time, datetime

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

    for booking in bookings:
        booking_start_time = time_from_offset_aware_to_naive(booking.start_time)
        booking_end_time = time_from_offset_aware_to_naive(booking.end_time)
        if (
            (booking_start_time <= start < booking_end_time)
            or (booking_start_time < end <= booking_end_time)
            or (start < booking_start_time and end > booking_end_time)
        ):
            return True

    return False


def convert_to_datetime(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, '%d-%m-%Y %H:%M:%S')
        return datetime_obj
    except ValueError as e:
        raise HTTPException(status_code=400, detail={'error': e})


def convert_date_format(date_str):
    try:
        # Parse the input date string
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')

        # Convert the date to the desired format
        converted_date_str = date_obj.strftime('%Y-%m-%d')

        return converted_date_str
    except ValueError as e:
        raise HTTPException(status_code=400, detail={'error': e})
