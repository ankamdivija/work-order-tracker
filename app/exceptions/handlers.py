
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.errors import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)

class WorkOrderNotFoundError(Exception):
    def __init__(self, work_order_id: int):
        self.work_order_id = work_order_id
        super().__init__(f"Work order {work_order_id} not found")

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        error_codes = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
        }

        code = error_codes.get(exc.status_code, "HTTP_ERROR")
        message = (
            exc.detail
            if isinstance(exc.detail, str)
            else "The request could not be completed"
        )

        body = ErrorResponse(
            error=ErrorDetail(
                code=code,
                message=message,
            )
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=body.model_dump(mode="json"),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        details = [
            {
                "field": ".".join(str(part) for part in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]

        body = ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                details=details,
            )
        )

        return JSONResponse(
            status_code=422,
            content=body.model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception("Unexpected error while processing request")

        body = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
            )
        )

        return JSONResponse(
            status_code=500,
            content=body.model_dump(mode="json"),
        )
    
    @app.exception_handler(WorkOrderNotFoundError)
    async def work_order_not_found_handler(
        request: Request,
        exc: WorkOrderNotFoundError,
    ):
        body = ErrorResponse(
            error=ErrorDetail(
                code="WORK_ORDER_NOT_FOUND",
                message=str(exc),
            )
        )

        return JSONResponse(
            status_code=404,
            content=body.model_dump(mode="json"),
        )