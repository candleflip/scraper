from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path

from app.api import crud
from app.models.pydantic.summary import SummaryPayloadSchema, SummaryResponseSchema, SummaryUpdatePayloadSchema
from app.models.tortoise.summary_schema import SummarySchema
from app.summarizer import generate_summary

router = APIRouter()


@router.post('/', response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema, background_tasks: BackgroundTasks) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    background_tasks.add_task(generate_summary, summary_id, payload.url)

    response_object = {'id': summary_id, 'url': payload.url}
    return response_object


@router.get('/{summary_id}/', response_model=SummarySchema)
async def read_summary(summary_id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(summary_id=summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.get('/', response_model=List[SummarySchema])
async def read_all_summaries() -> SummarySchema:
    summaries = await crud.get_all()
    return summaries


@router.delete('/{summary_id}/', response_model=SummaryResponseSchema)
async def delete_summary(summary_id: int = Path(..., gt=0)) -> SummaryResponseSchema:
    summary = await crud.get(summary_id=summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')

    await crud.delete(summary_id=summary_id)
    return summary


@router.put('/{summary_id}/', response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema,
    summary_id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.get(summary_id=summary_id)
    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')

    summary = await crud.put(summary_id=summary_id, payload=payload)
    return summary
