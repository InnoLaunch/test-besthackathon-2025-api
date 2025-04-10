from fastapi.responses import JSONResponse
from fastapi import Request

from core.exceptions.base import HTTPError


class HTTPErrorExceptionHandler:

    @staticmethod
    async def handle(request: Request, exc: HTTPError):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

