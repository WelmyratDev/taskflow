import logging
import time
import uuid

from fastapi import Request


logger = logging.getLogger(__name__)


async def request_logging_middleware(
    request: Request,
    call_next,
):
    request_id = request.headers.get(
        "X-Request-ID"
    ) or str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        status_code = response.status_code

    except Exception:
        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        logger.exception(
            "request_id=%s | %s %s | status=500 | %.2fms",
            request_id,
            request.method,
            request.url.path,
            response_time,
        )

        raise

    response_time = (
        time.perf_counter() - start_time
    ) * 1000

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = (
        f"{response_time:.2f}ms"
    )

    logger.info(
        "request_id=%s | %s %s | status=%s | %.2fms",
        request_id,
        request.method,
        request.url.path,
        status_code,
        response_time,
    )

    return response