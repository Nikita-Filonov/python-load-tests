from locust import events, task
from locust.env import Environment

from seeds.builder import get_seeds_builder
from seeds.dumps import save_seeds_result
from seeds.schema.plan import SeedsPlan, SeedOperationsPlan
from seeds.schema.result import SeedOperationResult
from tools.locust.task_set import BaseLocustTaskSet
from tools.locust.user import BaseLocustUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    builder = get_seeds_builder()
    result = builder.build(plan=SeedsPlan(operations=SeedOperationsPlan(count=20)))
    save_seeds_result(result=result, scenario="get_operations_with_seeds")

    environment.seeds = result


class GetOperationTaskSet(BaseLocustTaskSet):
    seed_operation: SeedOperationResult

    def on_start(self) -> None:
        super().on_start()

        self.seed_operation = self.user.environment.get_random_operation()

    @task(1)
    def get_operations(self):
        self.operations_client.get_operations()

    @task(3)
    def get_operation(self):
        self.operations_client.get_operation(self.seed_operation.operation_id)


class GetOperationUser(BaseLocustUser):
    tasks = [GetOperationTaskSet]
