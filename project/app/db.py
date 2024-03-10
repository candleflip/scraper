"""
Вспомогательный модуль для подготовки БД к работе приложения
"""
import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger('uvicorn')

# Конфигурация TortoiseORM для приложения
TORTOISE_ORM = {
    'connections': {'default': os.environ.get('DATABASE_URL')},
    'apps': {
        'models': {
            'models': ['app.models.tortoise.summary_schema', 'aerich.models'],
            'default_connection': 'default',
        }
    },
}


def initialize_database(app: FastAPI) -> None:
    """
    Инициализирует БД для приложения с моделями из файла Tortoise моделей

    Args:
        app: приложение, использующее БД

    """
    register_tortoise(
        app=app,
        db_url=os.environ.get('DATABASE_URL'),
        modules={'models': ['app.models.tortoise.summary_schema']},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    """
    Создание схемы по пути до файла с Tortoise моделями

    """
    log.info('Инициализация Tortoise...')
    await Tortoise.init(
        db_url=os.environ.get('DATABASE_URL'),
        modules={'models': ['models.tortoise.summary_schema']}
    )

    log.info('Генерация схемы БД через Tortoise...')
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == '__main__':
    run_async(generate_schema())
