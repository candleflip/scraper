from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()


@router.get('/health_check')
async def health_check(settings: Settings = Depends(get_settings)):
    return {'ping': 'pong', 'environment': settings.environment, 'testing': settings.testing}
