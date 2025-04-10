from http import HTTPStatus
from typing import Optional
from fastapi import HTTPException


HTTPException.default_status_status_code = HTTPStatus.BAD_REQUEST


class CustomHTTPException(HTTPException):
    status_code = HTTPStatus.BAD_REQUEST
    detail = HTTPStatus.BAD_REQUEST.description

    def __init__(self, detail: Optional[str] = None, headers: Optional[dict] = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=headers
        )


class BadRequestException(CustomHTTPException):
    status_code = HTTPStatus.BAD_REQUEST
    detail = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomHTTPException):
    status_code = HTTPStatus.NOT_FOUND
    detail = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomHTTPException):
    status_code = HTTPStatus.FORBIDDEN
    detail = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomHTTPException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomHTTPException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = HTTPStatus.UNPROCESSABLE_ENTITY.description


class ConflictException(CustomHTTPException):
    status_code = HTTPStatus.CONFLICT
    detail = HTTPStatus.CONFLICT.description


class MethodNotImplementedException(CustomHTTPException):
    status_code = HTTPStatus.NOT_IMPLEMENTED
    detail = HTTPStatus.NOT_IMPLEMENTED.description
