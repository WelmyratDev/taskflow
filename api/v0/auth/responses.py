from pydantic import BaseModel
from datetime import datetime


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str | None
    role: str
    created_at: datetime
    updated_at: datetime
