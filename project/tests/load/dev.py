from __future__ import annotations

from typing import Tuple, List

from locust import HttpUser, between, task, events, LoadTestShape, User


class WebUser(HttpUser):
    wait_time = between(1, 5)
    weight = 3
    host = 'http://0.0.0.0:8004'

    @task
    def health_check(self):
        self.client.get('/health_check/')


# class StageShape(LoadTestShape):
#     stages = [
#         {'duration': 20, 'users': 2, 'spawn_rate': 1},
#         {'duration': 40, 'users': 4, 'spawn_rate': 1},
#         {'duration': 60, 'users': 8, 'spawn_rate': 1},
#         {'duration': 80, 'users': 16, 'spawn_rate': 1},
#         {'duration': 100, 'users': 20, 'spawn_rate': 1},
#     ]
#
#     def tick(self) -> Tuple[int, float] | Tuple[int, float, List[type[User]] | None] | None:
#         run_time = self.get_run_time()
#
#         for stage in self.stages:
#             if run_time < stage['duration']:
#                 tick_data = (stage['users'], stage['spawn_rate'])
#                 return tick_data
#             return None


@events.test_start.add_listener
def ot_test_start(environment):
    print('A new test is starting...')


@events.test_stop.add_listener
def ot_test_stop(environment):
    print('A new test is stopping...')
