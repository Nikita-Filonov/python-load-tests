from locust import User, between


class BaseLocustUser(User):
    host = "localhost"
    abstract = True
    wait_time = between(1, 3)
