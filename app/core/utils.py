from typing import Callable

from fastapi import FastAPI
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
