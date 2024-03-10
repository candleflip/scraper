"""
Модуль тестирования ручки /summaries

Здесь собраны тесты с моком на фоновую задачу генерации пересказа.
Мока на поход в БД нет.

"""
import json

import pytest

from app.api import summaries


def test_create_summary(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на создание пересказа и замоканной фоновой задачей на генерацию пересказа
    WHEN: получает запрос на создание пересказа текста по URL с валидными параметрами
    THEN: создает пересказ в БД и возвращает положительный ответ со статус-кодом 201

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    assert response.json()['url'] == 'https://foo.bar'


def test_create_summary_invalid_json(test_app_with_db):
    """
    GIVEN: тестовое приложение с ручкой на создание пересказа
    WHEN: получает запрос на создание пересказа текста по URL с невалидным json (пустым либо с невалидным URL)
    THEN: возвращает ответ 422 с описанием

    """
    response = test_app_with_db.post('/summaries/', data=json.dumps({}))
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

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'invalid://url'}))
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'URL scheme not permitted'


def test_read_summary(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на получение пересказа по ID и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос на получение существующего в БД и валидного пересказа по ID
    THEN: возвращает ответ 200 с данными о пересказе

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app_with_db.get(f'/summaries/{summary_id}/')
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict['id'] == summary_id
    assert response_dict['url'] == 'https://foo.bar'
    assert response_dict['summary'] == ''
    assert response_dict['created_at']


def test_read_summary_incorrect_id(test_app_with_db):
    """
    GIVEN: тестовое приложение с ручкой на получение пересказа по ID
    WHEN: получает запрос на получение пересказа с невалидным ID (не существующего в
        БД, либо не представляющего логическую ценность)
    THEN: возвращает ответ 404 с телом описания либо 422, соответственно

    """
    response = test_app_with_db.get('/summaries/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Summary not found'

    response = test_app_with_db.get('/summaries/0/')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['path', 'summary_id'],
                'msg': 'ensure this value is greater than 0',
                'type': 'value_error.number.not_gt',
                'ctx': {'limit_value': 0},
            }
        ]
    }


def test_read_all_summaries(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на получение всех пересказов и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос на получение всех пересказов
    THEN: возвращает список с точным числом ранее созданных пересказов и статус-кодом 200

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    added_summaries = []
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo1.bar'}))
    assert response.status_code == 201
    added_summaries.append(response.json()['id'])
    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo2.bar'}))
    assert response.status_code == 201
    added_summaries.append(response.json()['id'])

    response = test_app_with_db.get('/summaries/')
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda x: x['id'] in added_summaries, response_list))) == 2


def test_remove_summary(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на удаление пересказа по ID и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос на удаление пересказа по ID
    THEN: удаляет ранее добавленный в БД пересказ со статус-кодом 200

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app_with_db.delete(f'/summaries/{summary_id}/')
    assert response.status_code == 200
    assert response.json() == {'id': summary_id, 'url': 'https://foo.bar'}


def test_remove_summary_incorrect_id(test_app_with_db):
    """
    GIVEN: тестовое приложение с ручкой на удаление пересказа по ID
    WHEN: получает запрос на удаление пересказа по невалидному ID (несуществующему в БД
        либо не представляющую логической ценности)
    THEN: возвращает 404 ошибку с описанием

    """
    response = test_app_with_db.delete('/summaries/999/')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Summary not found'

    response = test_app_with_db.delete('/summaries/0/')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['path', 'summary_id'],
                'msg': 'ensure this value is greater than 0',
                'type': 'value_error.number.not_gt',
                'ctx': {'limit_value': 0},
            }
        ]
    }


def test_update_summary(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на обновление пересказа по ID и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос на обновление ранее созданного валидного пересказа
    THEN: обновляет пересказ со статус-кодом 200

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app_with_db.put(
        f'/summaries/{summary_id}/',
        data=json.dumps({'url': 'https://foo.bar', 'summary': 'Updated summary'})
    )
    assert response.status_code == 200

    response = test_app_with_db.get(f'/summaries/{summary_id}/')
    assert response.status_code == 200
    summary_info = response.json()
    assert summary_info['id'] == summary_id
    assert summary_info['url'] == 'https://foo.bar'
    assert summary_info['summary'] == 'Updated summary'
    assert summary_info['created_at']


def test_update_summary_invalid_url(test_app_with_db, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на обновление пересказа по ID и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос с невалидным URL на обновление ранее созданного валидного пересказа
    THEN: возвращает ошибку 422 с описанием

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app_with_db.put(
        f'/summaries/{summary_id}/', data=json.dumps({'url': 'invalid://url', 'summary': 'Updated summary'})
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'URL scheme not permitted'


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
def test_update_summary_invalid(test_app_with_db, id_, payload, status_code, detail, monkeypatch):
    """
    GIVEN: тестовое приложение с ручкой на обновление пересказа по ID и замоканной фоновой
        задачей на генерацию пересказа
    WHEN: получает запрос на обновление пересказа с невалидным ID (не созданным, либо
        не представляющим логическую ценность)
    THEN: возвращает 422 ошибку с соответствующим описанием, объясняющим, почему ID не может
        быть использован на удаления

    """

    async def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, 'generate_summary', mock_generate_summary)

    response = test_app_with_db.post('/summaries/', data=json.dumps({'url': 'https://foo.bar'}))
    assert response.status_code == 201
    summary_id = response.json()['id']

    response = test_app_with_db.put(f'/summaries/{id_ if id_ in (0, 999) else summary_id}/', data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()['detail'] == detail
