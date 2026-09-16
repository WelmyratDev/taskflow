from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Account:
    id: int
    username: str
    email: str
    password: str
    last_activity: datetime
    created_at: datetime
    updated_at: datetime
    role: str
    
    def validate(self) -> None:
        self._validate_username()
        self._validate_email()

    def _validate_username(self) -> None:
        username = self.username.strip()

        if not username:
            raise ValueError("Username cannot be empty")

        if not 3 <= len(username) <= 50:
            raise ValueError(
                "Username must be between 3 and 50 characters"
            )

        if not re.fullmatch(
            r"[a-zA-Z0-9_.-]+",
            username,
        ):
            raise ValueError(
                "Username contains invalid characters"
            )

    def _validate_email(self) -> None:
        email = self.email.strip()

        if not email:
            raise ValueError("Email cannot be empty")

        if len(email) > 254:
            raise ValueError(
                "Email must be at most 254 characters"
            )

        if not re.fullmatch(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email,
        ):
            raise ValueError("Invalid email address")
