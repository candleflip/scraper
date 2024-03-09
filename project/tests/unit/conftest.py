"""
Модуль с набором фикстур для тестирования.

Использовать в файлах с unit-тестами.

"""
import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.settings import Settings, get_settings
from app.main import create_application


def get_settings_override():
    """
    Заменить настройки для тестовой среды

    Returns:
        Тестовые настройки.

    """
    return Settings(testing=1, database_url=os.environ.get('DATABASE_TEST_URL'))


@pytest.fixture(scope='module')
def test_app():
    """
    Подготовить экземпляр тестового приложения

    Создать приложение, передать тестовые настройки и создать клиент
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
    Подготовить экземпляр тестового приложения с БД

    Создать приложение, передать тестовые настройки и подготовить тестовую БД.
    А также создать клиент для тестирования работы приложения.

    Returns:
        Клиент для тестирования приложения с БД

    """
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app=app,
        db_url=os.environ.get('DATABASE_TEST_URL'),
        modules={'models': ['app.models.tortoise']},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
