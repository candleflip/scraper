from typing import List, Optional, Dict

from app.models.pydantic import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.tortoise import TextSummary
from app.summarizer import generate_summary


async def post(payload: SummaryPayloadSchema) -> int:
    article_summary = generate_summary(url=payload.url)
    summary = TextSummary(url=payload.url, summary=article_summary)
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
