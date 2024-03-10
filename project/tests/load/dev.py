"""
Модуль конфигурации нагрузочного тестирования в Locust

URL с интерфейсом: http://localhost:8005
"""
from __future__ import annotations
import logging

from locust import HttpUser, between, events, task

log = logging.getLogger('locust')


class WebUser(HttpUser):
    """
    Класс конфигурации пользователей, генерируемых для нагрузочного теста.

    wait_time: ожидание между соседними запросами от экземпляров пользователей,
        созданных из этого класса (в секундах)
    weight: вес данного типа пользователей в системе
    host: хост, по которому находится тестируемое приложение

    """
    wait_time = between(1, 5)
    weight = 3
    host = 'http://0.0.0.0:8005'

    @task
    def health_check(self):
        self.client.get('/health_check/')


@events.test_start.add_listener
def ot_test_start(environment):
    """
    Логирует начало теста.

    """
    log.info('Старт нового нагрузочного теста...')


@events.test_stop.add_listener
def ot_test_stop(environment):
    """
    Логирует окончание теста.

    """
    log.info('Остановка нагрузочного теста...')
