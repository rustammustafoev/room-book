from typing import Union
from datetime import date as datetime_date

from fastapi import APIRouter, Query, Path, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from tortoise.expressions import Q

from app.core import utils, helpers
from app.db import models
from app.db.schemas import room as room_schemas
from app.db.schemas import booking as booking_schemas
from app.db.schemas.pagination import PaginatedResponse

router = APIRouter()


@router.get('/', response_model=PaginatedResponse[room_schemas.RoomOut])
async def get_rooms(
        search: Union[str, None] = Query(None, title='Room name'),
        type: Union[str, None] = Query(None, title='Room type'),
        q: helpers.SimplePaginationParams = Depends(),
):
    filters = []
    if search:
        filters.append(Q(name=search))
    if type:
        filters.append(Q(type=type))

    rooms_query = models.Room.filter(Q(*filters, join_type='AND'))
    count = await rooms_query.count()
    rooms = await rooms_query.limit(q.limit).offset(q.offset)

    response = {
        'page': q.page,
        'count': count,
        'page_size': q.page_size,
        'results': rooms
    }

    return response


@router.get('/{room_id}', response_model=room_schemas.RoomOut)
async def get_room(room_id: int = Path(..., title='Room ID', gt=0)):
    room = await models.Room.get_or_none(id=room_id)

    if room is None:
        return JSONResponse({'error': 'topilmadi'}, status_code=404)

    return room


@router.post('/', response_model=room_schemas.RoomOut, status_code=201)
async def create_room(
        room_form: room_schemas.RoomIn = Body(..., example=room_schemas.RoomInExample)
):
    room = await models.Room.create(**jsonable_encoder(room_form))

    return room


@router.delete('/{room_id}', status_code=204)
async def delete_room(room_id: int = Path(..., gt=0)):
    room = await models.Room.get_or_none(id=room_id)

    if not room:
        raise HTTPException(status_code=404, detail='Room is not found')

    await room.delete()

    return JSONResponse('Room is deleted', status_code=204)


@router.get('/{room_id}/availability')
async def get_room_availability(
        room_id: int = Path(..., title='Room ID', gt=0),
        date: Union[str, None] = Query(default=None,
                                       title='Room availability at date',
                                       description='Format: DD-MM-YYYY',
                                       example='25-06-2023', )
):
    if date is not None:
        date = utils.convert_date_format(date)
    else:
        date = datetime_date.today()
    room = await models.Room.get_or_none(id=room_id)

    if not room:
        raise HTTPException(status_code=400, detail={'error': 'Room is not found'})

    bookings = await models.Booking.filter(room=room, date=date).order_by('start_time')

    available_time_slots = utils.get_available_time_slots(date, bookings)

    return available_time_slots


@router.post('/{room_id}/book')
async def book_room(
        room_id: int = Path(..., title='Room ID', gt=0),
        booking_form: booking_schemas.BookingIn = Body(..., title='Booking Form')
):
    room = await models.Room.get_or_none(id=room_id)
    resident = await models.Resident.get_or_none(name=booking_form.resident.name)

    if not room:
        raise HTTPException(status_code=400, detail={'error': 'Room is not found'})

    if not resident:
        raise HTTPException(status_code=400, detail={'error': 'Resident is not found'})

    start = utils.convert_to_datetime(booking_form.start)
    end = utils.convert_to_datetime(booking_form.end)

    if start.date() != end.date():
        raise HTTPException(status_code=400, detail={'error': 'Inconsistent dates'})

    date = start.date()

    bookings = await models.Booking.filter(room=room, date=date).order_by('start_time')

    # Perform a check between current booking and the ones that already reserved
    if utils.check_booking_time_for_clash(start, end, bookings):
        return JSONResponse({'error': 'uzr, siz tanlagan vaqtda xona band'}, status_code=410)

    # Creating new room booking
    await models.Booking.create(room=room, resident=resident, start_time=start, end_time=end, date=date)

    return JSONResponse({'message': 'xona muvaffaqiyatli band qilindi'}, status_code=201)
