from fastapi import APIRouter

from app.api.endpoints import bookings, residents, rooms


api_router = APIRouter()
api_router.include_router(bookings.router, prefix='/bookings', tags=['Booking'])
api_router.include_router(residents.router, prefix='/residents', tags=['Resident'])
api_router.include_router(rooms.router, prefix='/rooms', tags=['Room'])
