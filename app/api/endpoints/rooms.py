from typing import Union

from fastapi import APIRouter, Query, Path, HTTPException, Depends, Body
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q

from app.core import utils, helpers
from app.db import models
from app.db.schemas import room as room_schemas
from app.db.schemas import booking as booking_schemas
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


@router.post('/', response_model=room_schemas.RoomOut, status_code=201)
async def create_room(room_form: room_schemas.RoomIn):
    room = await models.Room.create(**jsonable_encoder(room_form))

    return room


@router.get('/{room_id}/availability')
async def get_room_availability(
    room_id: int = Path(..., title='Room ID', gt=0),
    date: Union[str, None] = Query(default=None,
                                   title='Room availability at date',
                                   description='Format: YYYY-MM-DD',
                                   example='2023-06-12',)
):
    date = utils.is_valid_date(date)
    room = await models.Room.get_or_none(id=room_id)

    if not room:
        raise HTTPException(status_code=400, detail={'error': 'Room is not found'})

    bookings = await models.Booking.filter(room=room, date=date).order_by('start_time')

    available_time_slots = utils.get_available_time_slots(room.opens_at, room.closes_at, bookings)

    return available_time_slots


@router.post('/{room_id}/book', response_model=booking_schemas.BookingOut)
async def book_room(
        room_id: int = Path(..., title='Room ID', gt=0),
        booking_form: booking_schemas.BookingIn = Body(...)
):
    room = await models.Room.get_or_none(idbooking_form=room_id)
    resident = await models.Resident.get_or_none(name=booking_form.resident)

    if not room:
        raise HTTPException(status_code=400, detail={'error': 'Room is not found'})

    if not resident:
        raise HTTPException(status_code=400, detail={'error': 'Resident is not found'})

    bookings = await models.Booking.filter(room=room, date=booking_form.date)

    if not utils.check_booking_time_for_clash(booking_form.start_time,
                                              booking_form.end_time,
                                              bookings):
        raise HTTPException(status_code=410, detail={'detail': 'Sorry, this room is fully booked'})

    new_booking = await models.Booking.create(
        room=room, resident=resident, start_time=booking_form.start_time,
        end_time=booking_form.end_time, date=booking_form.date
    )

    return new_booking

