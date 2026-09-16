from domain.repositories.session_account.session_account_pg_repos import (
    SessionAccountPgRepository
)
from domain.repositories.account.account_pg_repos import (
    AccountPgRepository
)
from domain.enterprise.account import session_entity
from domain.enterprise.account import entity as account_entity
from infrastructure.fastapi.exceptions import AppException
from shared.error import ErrorType
from shared.security import hash_password, hash_session_token, verify_password
from shared.utils import generate_session_token, verify_session_token
from typing import Callable
from datetime import timezone, timedelta

exception_tag = "AuthSession"


class AuthSession:

    def __init__(self, 
        session_repo: SessionAccountPgRepository,
        account_repo: AccountPgRepository
    ):
        self._session_repo = session_repo
        self._account_repo = account_repo
    
    async def create_session(self, account_id: int, response: Callable):
        session_token = generate_session_token()
        session_token_hash = hash_session_token(session_token)
        expires_at = timezone.now() + timedelta(days=30)
        
        try:
            new_session = await self._session_repo.create_account_session(
                account_id=account_id,
                session_token_hash=session_token_hash,
                expires_at=expires_at
            )
            response.set_cookie(
                key="session_id",
                value=session_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=60 * 60 * 24 * 30,
                path="/",
            )
            return new_session
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.create_session",
                msg=f"Session validation failed: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

            
    async def login(self,
        username: str,
        password: str,
        response: Callable
    ):
        try:
            account = account_entity.Account(
                username=username,
                password=password
            )
            account.validate()
            existing_account = await self._account_repo.get_by_username_and_email(
                username=account.username
            )
            if existing_account:
                if verify_password(
                    password=password,
                    password_hash=existing_account.password
                ):
                    await self.create_session(
                        account_id=existing_account.id,
                        response=response
                    )
                else:
                    raise AppException(
                        loc=f"{exception_tag}.login",
                        msg=f"Wrong password error: {e}",
                        type=ErrorType.INTERNAL_SERVER_ERROR,
                    )
            else:
                raise AppException(
                    loc=f"{exception_tag}.login",
                    msg=f"You should create account: {e}",
                    type=ErrorType.INTERNAL_SERVER_ERROR,
                )
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.login",
                msg=f"Something went wrong: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            )               

    async def register_account(self,
        username: str,
        email: str,
        password: str,
        role: str
    ):
        try:
            account = account_entity.Account(
                username=username,
                email=email,
                password=password,
                role=role
            )
            account.validate()
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.register_account",
                msg=f"Account validation failed: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        password_hash = hash_password(account.password)

        try:
            new_account = await self._account_repo.create(
                username=account.username,
                email=account.email,
                password_hash=password_hash,
                role=account.role
            )
        except AppException as e:
            raise AppException(
                loc=f"{exception_tag}.register_account",
                msg=f"Failed to register account: {e.detail['detail'][0]['msg']}",
                type=e.detail['detail'][0]['type'],
            ) from e

        try:
            return_account = account_entity.Account(
                id=new_account.id,
                username=new_account.username,
                email=new_account.email,
                password=new_account.password,
                last_activity=new_account.last_activity,
                created_at=new_account.created_at,
                role=new_account.role,
                updated_at=new_account.updated_at
            )
        except Exception as e:
            raise AppException(
                loc=f"{exception_tag}.register_account",
                msg=f"Failed to create account: {e}",
                type=ErrorType.INTERNAL_SERVER_ERROR,
            ) from e

        return return_account