from locust import TaskSet, SequentialTaskSet

from clients.operations_client import OperationsClient, get_operations_locust_client


class BaseLocustTaskSet(TaskSet):
    operations_client: OperationsClient

    def on_start(self) -> None:
        self.operations_client = get_operations_locust_client(self.user.environment)


class BaseLocustSequentialTaskSet(SequentialTaskSet):
    operations_client: OperationsClient

    def on_start(self) -> None:
        self.operations_client = get_operations_locust_client(self.user.environment)
