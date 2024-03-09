from typing import Dict, List, Optional

from app.models.pydantic.summary import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.tortoise.summary_schema import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary='')
    await summary.save()
    return summary.id


async def get(summary_id: int) -> Optional[Dict]:
    summary = await TextSummary.filter(id=summary_id).first().values()
    if not summary:
        return None
    return summary


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(summary_id: int) -> int:
    summary = await TextSummary.filter(id=summary_id).delete()
    return summary


async def put(summary_id: int, payload: SummaryUpdatePayloadSchema) -> Optional[Dict]:
    summary = await TextSummary.filter(id=summary_id).update(url=payload.url, summary=payload.summary)
    if not summary:
        return None

    updated_summary = await TextSummary.filter(id=summary_id).first().values()
    return updated_summary
