from locust import task

from schema.operations import OperationSchema
from tools.locust.task_set import BaseLocustSequentialTaskSet
from tools.locust.user import BaseLocustUser


class GetOperationSequentialTaskSet(BaseLocustSequentialTaskSet):
    operation: OperationSchema | None = None

    @task
    def create_operation(self):
        self.operation = self.operations_client.create_operation()

    @task
    def get_operations(self):
        self.operations_client.get_operations()

    @task
    def get_operation(self):
        if not self.operation:
            return

        self.operations_client.get_operation(self.operation.id)


class GetOperationUser(BaseLocustUser):
    tasks = [GetOperationSequentialTaskSet]
