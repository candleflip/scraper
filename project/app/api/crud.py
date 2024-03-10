"""
Модуль с CRUD-операциями для ручек /summaries
"""
from typing import Dict, List, Optional

from app.models.pydantic.summary import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.tortoise.summary_schema import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    """
    Добавить пересказ в БД

    Args:
        payload: объект пересказа с его URL

    Returns:
        ID созданного пересказа

    """
    summary = TextSummary(url=payload.url, summary='')
    await summary.save()
    return summary.id


async def get(summary_id: int) -> Optional[Dict]:
    """
    Получить пересказ из БД по его ID

    Args:
        summary_id: ID получаемого пересказа

    Returns:
        (Опционально) кортеж данных пересказа из БД

    """
    summary = await TextSummary.filter(id=summary_id).first().values()
    if not summary:
        return None
    return summary


async def get_all() -> List:
    """
    Получить все пересказы из БД

    Returns:
        Список пересказов, существующих в БД

    """
    summaries = await TextSummary.all().values()
    return summaries


async def delete(summary_id: int) -> int:
    """
    Удалить пересказ из БД по его ID

    Args:
        summary_id: ID удаляемого пересказа

    Returns:
        Кортеж данных об удаленном пересказе из БД

    """
    summary = await TextSummary.filter(id=summary_id).delete()
    return summary


async def put(summary_id: int, payload: SummaryUpdatePayloadSchema) -> Optional[Dict]:
    """
    Обновить пересказ в БД по его ID

    Args:
        summary_id: ID обновляемого пересказа
        payload: новые данные для пересказа, которыми необходимо заменить старую версию

    Returns:
        Обновленный кортеж с данными о пересказе из БД

    """
    summary = await TextSummary.filter(id=summary_id).update(url=payload.url, summary=payload.summary)
    if not summary:
        return None

    updated_summary = await TextSummary.filter(id=summary_id).first().values()
    return updated_summary
