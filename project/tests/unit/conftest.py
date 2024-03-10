"""
Модуль с набором фикстур для тестирования

Используется в файлах с unit-тестами.

"""
import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import create_application
from app.settings import Settings, get_settings


def get_settings_override():
    """
    Заменяет настройки для тестовой среды

    Returns:
        Тестовые настройки.

    """
    return Settings(testing=1, database_url=os.environ.get('DATABASE_TEST_URL'))


@pytest.fixture(scope='module')
def test_app():
    """
    Подготавливает экземпляр тестового приложения

    Создает приложение, передает тестовые настройки и создает клиента
    для тестирования его работы.

    Returns:
        Клиент для тестирования приложения

    """
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='module')
def test_app_with_db():
    """
    Подготавливает экземпляр тестового приложения с БД

    Создает приложение, передает тестовые настройки и подготавливает тестовую БД.
    А также создает клиент для тестирования работы приложения.

    Returns:
        Клиент для тестирования приложения с БД

    """
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app=app,
        db_url=os.environ.get('DATABASE_TEST_URL'),
        modules={'models': ['app.models.tortoise.summary_schema']},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
