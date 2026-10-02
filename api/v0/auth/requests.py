from pydantic import BaseModel
from fastapi import Form

from api.enums.account import UserRole


class RegisterUserRequest(BaseModel):
    username: str
    email: str | None
    password: str
    role: UserRole

    @classmethod
    def as_form(
        cls,
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        role: UserRole = Form(),
    ):
        return cls(
            username=username,
            email=email,
            password=password,
            role=role,
        )


