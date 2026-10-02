from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from shared.logging.logger import setup_logging
from infrastructure.fastapi.middleware.request_logging import request_logging_middleware
from infrastructure.asyncpg import Asyncpg
from api.controllers import router as main_router
import time
import logging


APP_TITLE = "TaskFlow Backend"
VERSION = "1.0.0"

setup_logging()

logger = logging.getLogger(__name__)

db = Asyncpg()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    logger.info(
        "Starting %s v%s",
        APP_TITLE,
        VERSION,
    )
    await db.connect()
    logger.info("PostgreSQL connection pool initialized")
    yield
    # Shutdown code here
    await db.close()
    logger.info("PostgreSQL connection pool closed")
    logger.info(
        "Stopping %s",
        APP_TITLE,
    )


app = FastAPI(
    title=APP_TITLE,
    version=VERSION,
    lifespan=lifespan,
)

app.middleware("http")(
    request_logging_middleware
)

@app.get("/")
def root(request: Request):
    return {
        "message": "TaskFlow Backend is running",
        "request_id": request.state.request_id,
    }


app.include_router(main_router)