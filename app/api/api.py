from fastapi import APIRouter

from app.api.endpoints import bookings, residents, rooms


api_router = APIRouter(tags=['Room Booking'])
api_router.include_router(bookings.router, prefix='/booking')
api_router.include_router(residents.router, prefix='/resident')
api_router.include_router(rooms.router, prefix='/room')
