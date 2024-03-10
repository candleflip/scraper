"""
Модуль тестирования ручки /summaries

Здесь собраны тесты с моком на фоновую задачу генерации пересказа, а также с моком на поход в БД.

"""
import json
from datetime import datetime

import pytest

from app.api import crud, summaries


def test_create_summary(test_app, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на создание пересказа и замоканными
походом в БД и фоновой задачей на генерацию пересказа
    WHEN: получает запрос на создание пересказа текста по URL с валидными параметрами
    THEN: возвращает положительный ответ со статус-кодом 201

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    test_request_payload = {'url': 'https://foo.bar'}
    test_response_payload = {'id': 1, 'url': 'https://foo.bar'}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, 'post', mock_post)

    response = test_app.post('/summaries/', data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summary_invalid_json(test_app):
    """
    GIVEN: тестовое приложение с ручкой на создание пересказа
    WHEN: получает запрос на создание с невалидным json (пустым либо содержащим невалидный URL)
    THEN: возвращает ошибку 422 с описанием

    """
    response = test_app.post('/summaries/', data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'url'],
                'msg': 'field required',
                'type': 'value_error.missing',
            }
        ]
    }

    response = test_app.post('/summaries/', data=json.dumps({'url': 'invalid://url'}))
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'URL scheme not permitted'


def test_read_summary(test_app, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на получение пересказа по ID и замоканным походом в БД
    WHEN: получает запрос на получение существующего в БД и валидного пересказа по ID
    THEN: возвращает ответ 200 с данными о пересказе

    """
    test_data = {'id': 1, 'url': 'https://foo.bar', 'summary': 'summary', 'created_at': datetime.utcnow().isoformat()}

    async def mock_get(summary_id):
        return test_data

    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/summaries/1/')
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на получение пересказа по ID и замоканным походом в БД
    WHEN: получает запрос на получение пересказа, не существующего в БД
    THEN: возвращает ответ 404 с телом описания

    """

    async def mock_get(summary_id):
        return None

    monkeypatch.setattr(crud, 'get', mock_get)

    response = test_app.get('/summaries/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Summary not found'


def test_read_all_summaries(test_app):
    pass


def test_remove_summary(test_app):
    pass


def test_remove_summary_incorrect_id(test_app):
    pass


def test_update_summary(test_app):
    pass


@pytest.mark.parametrize(
    'id_, payload, status_code, detail',
    [
        [999, {'url': 'https://foo.bar', 'summary': 'Updated summary'}, 404, 'Summary not found'],
        [
            0,
            {'url': 'https://foo.bar', 'summary': 'Updated summary'},
            422,
            [
                {
                    'ctx': {'limit_value': 0},
                    'loc': ['path', 'summary_id'],
                    'msg': 'ensure this value is greater than 0',
                    'type': 'value_error.number.not_gt',
                },
            ],
        ],
        [
            1,
            {},
            422,
            [
                {'loc': ['body', 'url'], 'msg': 'field required', 'type': 'value_error.missing'},
                {'loc': ['body', 'summary'], 'msg': 'field required', 'type': 'value_error.missing'},
            ],
        ],
        [
            1,
            {'url': 'https://foo.bar'},
            422,
            [{'loc': ['body', 'summary'], 'msg': 'field required', 'type': 'value_error.missing'}],
        ],
    ],
)
def test_update_summary_invalid(test_app, id_, payload, status_code, detail):
    pass


def test_update_summary_invalid_url(test_app, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на изменение пересказа по ID и замоканными
        походом в БД и фоновой задачей на генерацию пересказа
    WHEN: получает запрос на изменение существующего в БД пересказа, но в запросе невалидный URL
    THEN: возвращает ответ 422 с описанием, что URL невалиден

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, 'post', mock_post)

    response = test_app.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app.put(
        f'/summaries/{summary_id}/', data=json.dumps({'url': 'invalid://url', 'summary': 'Updated summary'})
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'URL scheme not permitted'
