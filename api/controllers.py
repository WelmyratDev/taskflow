from fastapi import APIRouter, Depends

from .v0.controllers import router as v0_router

router = APIRouter(
    prefix='/api'
)

router.include_router(v0_router)