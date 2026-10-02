from fastapi import APIRouter, Depends

from .auth.controllers import router as auth_router


from . import API_VERSION

router = APIRouter(
    prefix=f"/{API_VERSION}",
)


router.include_router(auth_router, tags=["auth"])


