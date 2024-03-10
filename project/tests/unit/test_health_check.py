"""
Модуль тестирования ручки /health_check
"""


def test_health_check(test_app):
    """
    GIVEN: тестовое приложение с ручкой для проверки работы сервиса
    WHEN: получает GET запрос на проверку работы сервиса
    THEN: возвращает ответ со статус-кодом 200 и информацией о параметрах приложения

    """
    response = test_app.get('/health_check')
    assert response.status_code == 200
    assert response.json() == {'ping': 'pong', 'environment': 'dev', 'testing': True}
