from typing import Union

from fastapi import APIRouter, Query, Depends, Path, HTTPException, Form
from fastapi.responses import JSONResponse
from tortoise.expressions import Q

from app.core import helpers
from app.db import models
from app.db.schemas import booking as booking_schemas
from app.db.constants import BookingStatus


router = APIRouter()


@router.get('/')
async def get_bookings(
        q: helpers.PaginationParams = Depends(),
        booking_status: Union[BookingStatus, None] = Query(None, title='Booking status')
):
    filters = []
    if booking_status:
        filters.append(Q(status=booking_status))
    booking_query = models.Booking.filter(Q(*filters, join_type='AND'))

    count = await booking_query.count()
    bookings = await booking_query.limit(q.limit).offset(q.offset)

    response = {'count': count, 'results': bookings}

    return response


@router.patch('/change/status/{booking_id}', response_model=booking_schemas.BookingOut)
async def change_booking_status(
    booking_id: int = Path(..., gt=0),
    booking_status: BookingStatus = Form(..., title='Booking status')
):
    booking = await models.Booking.get_or_none(id=booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail='Booking is not found')

    booking.status = booking_status
    await booking.save()

    return booking


@router.delete('/delete/{booking_id}', status_code=204)
async def delete_booking(booking_id: int = Path(..., gt=0)):
    booking = await models.Booking.get_or_none(id=booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail='Booking is not found')

    await booking.delete()

    return JSONResponse('Booking is deleted', status_code=204)
