from __future__ import annotations

from locust import HttpUser, between, events, task


class WebUser(HttpUser):
    wait_time = between(1, 5)
    weight = 3
    host = 'http://0.0.0.0:8005'

    @task
    def health_check(self):
        self.client.get('/health_check/')


@events.test_start.add_listener
def ot_test_start(environment):
    print('A new test is starting...')


@events.test_stop.add_listener
def ot_test_stop(environment):
    print('A new test is stopping...')
