from locust import HttpUser, task


class HealthCheck(HttpUser):
    @task
    def health_check(self):
        self.client.get('/health_check/')
