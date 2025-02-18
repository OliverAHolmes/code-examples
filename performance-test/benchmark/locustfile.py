from locust import HttpUser, task, between

class DRFUser(HttpUser):
    # Points to Django REST (port 8001)
    host = "http://localhost:8001"
    wait_time = between(1, 3)
    
    @task
    def hello_drf(self):
        # The DRF endpoint
        self.client.get("/django/?format=json")


class FastAPIUser(HttpUser):
    # Points to FastAPI (port 8002)
    host = "http://localhost:8002"
    wait_time = between(1, 3)
    
    @task
    def hello_fastapi(self):
        self.client.get("/fastapi")


class RobynUser(HttpUser):
    # Points to Robyn (port 8003)
    host = "http://localhost:8003"
    wait_time = between(1, 3)
    
    @task
    def hello_robyn(self):
        self.client.get("/robyn")

class ActixUser(HttpUser):
    host = "http://localhost:8004"
    wait_time = between(1, 3)

    @task
    def hello_actix(self):
        self.client.get("/actix-web")
