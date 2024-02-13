from fastapi import APIRouter, Depends

from app.config import get_settings, Settings

router = APIRouter()


@router.get('/health_check')
async def health_check(settings: Settings = Depends(get_settings)):
    return {
        'ping': 'pong',
        'environment': settings.environment,
        'testing': settings.testing
    }
