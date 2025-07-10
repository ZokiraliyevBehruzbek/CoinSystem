from pydantic import BaseModel
from typing import Optional

class Register(BaseModel):
    username: str
    password: str
    is_superuser: Optional[int] = None

class Login(BaseModel):
    username: str
    password: str
