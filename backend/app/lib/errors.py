# backend/app/lib/errors.py

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger("sentryflow")

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": request.url.path},
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request payload", "details": exc.errors()},
    )

async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    logger.error(f"Response validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal response serialization error", "details": exc.errors()},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
