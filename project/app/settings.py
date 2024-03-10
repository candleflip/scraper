"""
Файл конфигурации проекта

Имеет функционал сбора значений переменных окружения и их обработки
"""
import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger('uvicorn')


class Settings(BaseSettings):
    """
    Конфигурация проекта по переменным окружения

    """
    environment: str = os.getenv('ENVIRONMENT', 'dev')
    testing: bool = os.getenv('TESTING', 0)
    database_url: AnyUrl = os.environ.get('DATABASE_URL')


@lru_cache()
def get_settings() -> BaseSettings:
    """
    Получение экземпляра настроек для приложения

    Returns:
        Готовая конфигурация приложения

    """
    log.info('Загрузка настроек проекта из переменных окружения...')
    return Settings()
