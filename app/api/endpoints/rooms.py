from typing import Union

from fastapi import APIRouter, Query, Path

from app.core import utils

router = APIRouter()


@router.get('/')
async def get_rooms(
    search: Union[str, None] = Query(None, title='Room name'),
    room_type: Union[str, None] = Query(None, title='Room type'),
    page: int = Query(..., title='Page number'),
    page_size: int = Query(default=10, title='Number of results in a page')
):
    pass


@router.get('/{room_id}')
async def get_room(room_id: int = Path(..., title='Room ID', gt=1)):
    pass


@router.get('/{room_id}/availability')
async def get_room_availability(
    room_id: int = Path(..., title='Room ID', gt=1),
    date: Union[str, None] = Query(default=None,
                                   title='Room availability at date',
                                   description='Format: YYYY-MM-DD HH:MM:SS',
                                   example='2023-06-12 15:59:59',)
):
    date = utils.is_valid_date(date)


@router.get('/{room_id}/book')
async def book_room(room_id: int = Path(..., title='Room ID', gt=1)):
    pass
