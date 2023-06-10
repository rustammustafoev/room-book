
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_rooms():
    pass


@router.get('{room_id}')
async def get_room():
    pass


@router.get('{room_id}/availability')
async def get_room_availability():
    pass


@router.get('{room_id}/book')
async def book_room():
    pass
