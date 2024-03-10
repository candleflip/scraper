"""
Точка входа в приложение.

Создает приложение, принимает роутеры из модулей ручек.
"""
import logging

from fastapi import FastAPI

from app.api import health_check, summaries
from app.db import initialize_database

log = logging.getLogger('uvicorn')


def create_application() -> FastAPI:
    """
    Подготавливает приложение

    Создает экземпляр приложения, добавляет в него ручки.

    Returns:
        Сконфигурированное приложение.

    """
    application = FastAPI()
    application.include_router(health_check.router)
    application.include_router(summaries.router, prefix='/summaries', tags=['summaries'])

    return application


app = create_application()


@app.on_event('startup')
async def startup_event():
    """
    Инициализирует БД перед стартом работы приложения

    """
    log.info('Старт приложения...')
    log.info('Запуск БД.')
    initialize_database(app=app)
    log.info('БД инициализирована...')


@app.on_event('shutdown')
async def shutdown_event():
    """
    Логирует остановку приложения

    """
    log.info('Остановка приложения...')
