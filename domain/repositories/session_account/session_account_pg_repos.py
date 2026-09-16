from domain.enterprise.account import session_entity
from infrastructure.fastapi.exceptions import AppException
from datetime import datetime
from shared.error import ErrorType
import asyncpg


exception_tag = "SessionAccountPgRepository"


class SessionAccountPgRepository:

    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def create_account_session(self,
        account_id: int,
        session_token_hash: str,
        expires_at: datetime | None = None
    ):
        try:
            stmt_insert_clause = """
                INSERT INTO session_accounts (account_id, session_token_hash, expires_at)
                VALUES ($1, $2, $3)
                RETURNING id, account_id, session_token_hash, expires_at, created_at, updated_at
            """
            row = await self._conn.fetchrow(
                stmt_insert_clause,
                account_id,
                session_token_hash,
                expires_at
            )

        except asyncpg.PostgresError as e:
            raise AppException(
                loc=f"{exception_tag}.create_session_account",
                msg=f"Failed to create session account: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        if row is None:
            raise AppException(
                loc=f"{exception_tag}.create_session_account",
                msg="Failed to create session account",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            )

        try:
            return session_entity.AccountSession(
                id=row["id"],
                account_id=row["account_id"],
                session_token_hash=row["session_token_hash"],
                expires_at=row['expires_at'],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.create_session_account",
                msg=f"Failed to map database row to AccountSession entity: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e
    