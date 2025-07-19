import random

from pydantic import BaseModel, Field


class SeedOperationResult(BaseModel):
    operation_id: int


class SeedsResult(BaseModel):
    operations: list[SeedOperationResult] = Field(default_factory=list)

    def get_next_operation(self) -> SeedOperationResult:
        return self.operations.pop(0)

    def get_random_operation(self) -> SeedOperationResult:
        return random.choice(self.operations)
