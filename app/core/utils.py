from typing import Callable

from fastapi import FastAPI


def start_up_handler(app: FastAPI) -> Callable:
    async def start_up() -> None:
        pass

    return start_up


def shut_down_handler(app: FastAPI) -> Callable:
    async def shut_down() -> None:
        pass

    return shut_down
