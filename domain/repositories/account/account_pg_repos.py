from domain.enterprise.account import entity as account_entity
from infrastructure.fastapi.exceptions import AppException
from shared.error import ErrorType
import asyncpg



exception_tag = "AccountPgRepository"


class AccountPgRepository:

    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def create(self,
        username: str,
        email: str,
        password_hash: str,
        role: str,
    ):
        try:
            stmt_insert_clause = """
                INSERT INTO account (username, email, password, role)
                VALUES ($1, $2, $3, $4)
                RETURNING id, username, email, password, last_activity, created_at, updated_at, role
            """
            row = await self._conn.fetchrow(
                stmt_insert_clause,
                username,
                email,
                password_hash,
                role,
            )

        except asyncpg.UniqueViolationError as e:
            raise AppException(
                loc=f"{exception_tag}.create_account",
                msg="Account with this username or email already exists",
                type=ErrorType.CONFLICT,
            ) from e

        except asyncpg.PostgresError as e:
            raise AppException(
                loc=f"{exception_tag}.create_account",
                msg=f"Failed to create account: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        if row is None:
            raise AppException(
                loc=f"{exception_tag}.create_account",
                msg="Failed to create account",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            )

        try:
            return account_entity.Account(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password=row["password"],
                last_activity=row["last_activity"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                role=row["role"],
            )

        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.create_account",
                msg=f"Failed to create account entity: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e


    async def list_of_accounts(self) -> list[account_entity.Account]:
        
        try:
            stmt_select_clause = """
                SELECT id, username, email, password, last_activity, created_at, updated_at, role
                FROM account
            """
            accounts = await self._conn.fetch(stmt_select_clause)
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.list_of_accounts",
                msg=f"Failed to retrieve accounts: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        try:
            return [
                account_entity.Account(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    password=row["password"],
                    last_activity=row["last_activity"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    role=row["role"],
                )
                for row in accounts
            ]
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.list_of_accounts",
                msg=f"Failed to create account entities: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

    async def get_by_username_and_email(self, username: str, email: str) -> bool:
        try:
            stmt_select_clause = """
                SELECT 1
                FROM account
                WHERE username = $1 OR email = $2
                LIMIT 1
            """
            row = await self._conn.fetchrow(
                stmt_select_clause,
                username,
                email,
            )

        except asyncpg.PostgresError as e:
            raise AppException(
                loc=f"{exception_tag}.get_by_username_and_email",
                msg=f"Failed to check account existence: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        if row is None:
            return False

        try:
            account = account_entity.Account(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                password=row["password"],
                last_activity=row["last_activity"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                role=row["role"],
            )
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.get_by_username_and_email",
                msg=f"Failed to check account existence: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e
        return account