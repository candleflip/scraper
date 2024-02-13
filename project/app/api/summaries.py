from fastapi import APIRouter

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema

router = APIRouter()


@router.post('/', response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {
        'id': summary_id,
        'url': payload.url
    }
    return response_object


@router.get('/{id}/', response_model=SummarySchema)
async def read_summary(summary_id: int) -> SummarySchema:
    summary = crud.get(summary_id=summary_id)
    return summary
