from clients.operations_client import OperationsClient, get_operations_client
from seeds.schema.plan import SeedsPlan
from seeds.schema.result import SeedsResult, SeedOperationResult


class SeedsBuilder:
    def __init__(self, operations_client: OperationsClient):
        self.operations_client = operations_client

    def build_operation_result(self) -> SeedOperationResult:
        operation = self.operations_client.create_operation()
        return SeedOperationResult(operation_id=operation.id)

    def build(self, plan: SeedsPlan) -> SeedsResult:
        return SeedsResult(
            operations=[self.build_operation_result() for _ in range(plan.operations.count)]
        )


def get_seeds_builder():
    return SeedsBuilder(operations_client=get_operations_client())
