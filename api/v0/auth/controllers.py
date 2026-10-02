from fastapi import APIRouter, Depends, Request, Body
from infrastructure.dependencies.auth import build_auth_session_use_case
from api.dependencies import inject_apg_pool
from infrastructure.fastapi.exceptions import AppException
from shared.error import ErrorType
from . import requests, responses
from typing import Annotated, Callable
import asyncpg
import logging

router = APIRouter(
    prefix='/auth',
)

logger = logging.getLogger(__name__)

@router.post(
    path="/register",
    summary="Register a new user",
    description="Register a new user with the provided credentials.",
    tags=["auth"],
    response_model=responses.AccountResponse,
)
async def register_user_request(
    request: Request,
    input: Annotated[requests.RegisterUserRequest, Depends(requests.RegisterUserRequest.as_form)],
    db_pool: Annotated[asyncpg.Pool, Depends(inject_apg_pool)],
):
    logger.info("Registering new user: %s", input.username)
    try:
        async with db_pool.acquire() as conn:
            auth_use_case = build_auth_session_use_case(conn)
            new_account = await auth_use_case.register_account(
                username=input.username,
                email=input.email,
                password=input.password,
                role=input.role
            )
            return new_account
    except Exception as e:
        logger.exception("Error registering user")
        raise AppException(
            loc=f"Failed to register user: {e}",
            msg="The service is currently unavailable. Please try again later.",
            type=ErrorType.INTERNAL_SERVER_ERROR,
        ) from e
