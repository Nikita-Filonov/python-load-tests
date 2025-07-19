from httpx import Response
from locust.env import Environment

from clients.base_client import BaseClient, ClientExtensions, get_http_client, get_locust_http_client
from config import settings
from schema.operations import CreateOperationSchema, OperationSchema, OperationsSchema
from tools.routes import APIRoutes


class OperationsClient(BaseClient):
    def get_operations_api(self) -> Response:
        return self.get(APIRoutes.OPERATIONS)

    def get_operation_api(self, operation_id: int) -> Response:
        return self.get(
            f"{APIRoutes.OPERATIONS}/{operation_id}",
            extensions=ClientExtensions(route=f"{APIRoutes.OPERATIONS}/{{operation_id}}")
        )

    def create_operation_api(self, operation: CreateOperationSchema) -> Response:
        return self.post(
            APIRoutes.OPERATIONS,
            json=operation.model_dump(mode='json', by_alias=True)
        )

    def get_operations(self) -> OperationsSchema:
        response = self.get_operations_api()
        return OperationsSchema.model_validate_json(response.text)

    def get_operation(self, operation_id: int) -> OperationSchema:
        response = self.get_operation_api(operation_id)
        return OperationSchema.model_validate_json(response.text)

    def create_operation(self) -> OperationSchema:
        request = CreateOperationSchema()
        response = self.create_operation_api(request)
        return OperationSchema.model_validate_json(response.text)


def get_operations_client() -> OperationsClient:
    return OperationsClient(client=get_http_client(settings.fake_bank_http_client))


def get_operations_locust_client(environment: Environment) -> OperationsClient:
    return OperationsClient(
        client=get_locust_http_client(settings.fake_bank_http_client, environment)
    )
