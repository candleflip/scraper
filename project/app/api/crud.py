from typing import List, Optional

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary='dummy summary')
    await summary.save()
    return summary.id


async def get(summary_id: int) -> Optional[dict]:
    summary = await TextSummary.filter(id=summary_id).first().values()
    if summary:
        return summary
    return None


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(summary_id: int) -> int:
    summary = await TextSummary.filter(id=summary_id).delete()
    return summary
