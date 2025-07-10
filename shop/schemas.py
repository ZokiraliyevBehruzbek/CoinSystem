from pydantic import BaseModel
from typing import Optional

class CreateSchema(BaseModel):
    name: str
    description: str
    price: float

class PaginationSchema(BaseModel):
    page: int
    per_page: int

class RemoveSchemas(BaseModel):
    name: str
    is_superuser: Optional[int]