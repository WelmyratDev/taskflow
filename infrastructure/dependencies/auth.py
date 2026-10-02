from application.use_cases.auth.session_auth import AuthSessionUseCase
from domain.repositories.account.account_pg_repos import AccountPgRepository
from domain.repositories.session_account.session_account_pg_repos import SessionAccountPgRepository
import asyncpg



def build_auth_session_use_case(conn: asyncpg.Connection) -> AuthSessionUseCase:
    return AuthSessionUseCase(
        session_repo=SessionAccountPgRepository(conn=conn),
        account_repo=AccountPgRepository(conn=conn)
    )