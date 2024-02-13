from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post('/', response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {
        'id': summary_id,
        'url': payload.url
    }
    return response_object


@router.get('/{summary_id}/', response_model=SummarySchema)
async def read_summary(summary_id: int) -> SummarySchema:
    summary = await crud.get(summary_id=summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.get('/', response_model=List[SummarySchema])
async def read_all_summaries() -> SummarySchema:
    summaries = await crud.get_all()
    return summaries