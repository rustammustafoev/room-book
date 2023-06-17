from typing import Union

from fastapi import APIRouter, Query, Path, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q

from app.core import utils, helpers
from app.db import models
from app.db.schemas import room as room_schemas
from app.db.schemas.pagination import PaginatedPerPageResponse

router = APIRouter()


@router.get('/', response_model=PaginatedPerPageResponse[room_schemas.RoomOut])
async def get_rooms(
    search: Union[str, None] = Query(None, title='Room name'),
    room_type: Union[str, None] = Query(None, title='Room type'),
    q: helpers.PaginationParams = Depends(),
):
    filters = []
    if search:
        filters.append(Q(name=search))
    if room_type:
        filters.append(Q(type=room_type))

    rooms_query = models.Room.filter(Q(*filters, join_type='AND'))
    count = await rooms_query.count()
    items = await rooms_query.limit(q.limit).offset(q.offset)

    return helpers.paginate(q.page, q.per_page, count, items)


@router.get('/{room_id}', response_model=room_schemas.RoomOut)
async def get_room(room_id: int = Path(..., title='Room ID', gt=0)):
    room = await models.Room.get_or_none(id=room_id)

    if room is None:
        raise HTTPException(status_code=404, detail={'error': 'Room is not found'})

    return room


@router.post('/create', response_model=room_schemas.RoomOut)
async def create_room(room_form: room_schemas.RoomIn):
    room = await models.Room.create(**jsonable_encoder(room_form))

    return room


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
