
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from app.db.schemas.pagination import PaginatedPerPageResponse
from app.db.schemas import resident as resident_schemas
from app.db import models
from app.core import helpers

router = APIRouter()


@router.get('/', response_model=PaginatedPerPageResponse[resident_schemas.ResidentOut])
async def get_residents(
        q: helpers.PaginationParams = Depends(),
):
    residents_query = models.Resident.all()
    count = await residents_query.count()
    items = await residents_query.limit(q.limit).offset(q.offset)

    return helpers.paginate(q.page, q.per_page, count, items)


@router.get('/{resident_id}', response_model=resident_schemas.ResidentOut)
async def get_resident(resident_id: int):
    resident = await models.Resident.get_or_none(id=resident_id)

    if not resident:
        raise HTTPException(status_code=404, detail={'errors': 'Resident is not found'})

    return resident


@router.post('/', response_model=resident_schemas.ResidentOut, status_code=201)
async def create_resident(resident_form: resident_schemas.ResidentIn):
    resident = await models.Resident.create(**jsonable_encoder(resident_form))

    return resident
