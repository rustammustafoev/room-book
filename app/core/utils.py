from typing import Callable, Union
from datetime import datetime

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from loguru import logger

from app.core import tortoise_config


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
        datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return True

    except ValueError:
        return False


def is_valid_date(date: Union[str, None]) -> str:
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if date is None:
        date = current_date

    elif not check_date_format(date):
        raise HTTPException(status_code=400,
                            detail={'error': 'Date does not match format YYYY-MM-DD HH:MM:SS'})

    elif not (date > current_date):
        raise HTTPException(status_code=400,
                            detail={'error': 'Specified date must not be in the past!'})

    return date
