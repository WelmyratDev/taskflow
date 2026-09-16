from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


EXPIRES_DAYS = 7  # Default session expiration in days


@dataclass
class AccountSession:
    id: int
    account_id: int
    session_token_hash: str
    created_at: datetime
    expires_at: datetime | None
    last_activity: datetime | None
    ip_address: str
    user_agent: str

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def set_expiration(self, expires_in_days: int = EXPIRES_DAYS) -> None:
        self.expires_at = self.created_at + timedelta(days=expires_in_days)