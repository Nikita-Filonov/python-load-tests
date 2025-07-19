from pydantic import BaseModel, Field


class SeedOperationsPlan(BaseModel):
    count: int = 0


class SeedsPlan(BaseModel):
    operations: SeedOperationsPlan = Field(default_factory=SeedOperationsPlan)
