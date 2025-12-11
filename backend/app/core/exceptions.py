# app/core/exceptions.py
from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    """Базовое исключение API"""
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class NotFoundException(BaseAPIException):
    """Ресурс не найден"""
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, error_code=error_code)

class UnauthorizedException(BaseAPIException):
    """Не авторизован"""
    def __init__(self, detail: str = "Unauthorized", error_code: str = "UNAUTHORIZED"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, error_code=error_code)


class BadRequestException(BaseAPIException):
    """Некорректный запрос"""
    def __init__(self, detail: str = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, error_code=error_code)

class ConflictException(BaseAPIException):
    """Конфликт (уже существует)"""
    def __init__(self, detail: str = "Resource already exists", error_code: str = "CONFLICT"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, error_code=error_code)

# Специфичные для домена исключения
class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(detail="User not found", error_code="USER_NOT_FOUND")

class EmailAlreadyExistsException(ConflictException):
    def __init__(self):
        super().__init__(detail="Email already registered", error_code="EMAIL_EXISTS")

class InvalidCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__(detail="Invalid credentials", error_code="INVALID_CREDENTIALS")
class NotAuthenticatedException(UnauthorizedException):
    def __init__(self):
        super().__init__(detail="Not authenticated", error_code="NOT_AUTHENTICATED")

class ForbiddenException(BaseAPIException):
    """Доступ запрещен"""
    def __init__(self, detail: str = "Forbidden", error_code: str = "FORBIDDEN"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, error_code=error_code)