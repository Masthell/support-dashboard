# app/core/error_handlers.py
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from .exceptions import BaseAPIException  

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """Полная версия обработчиков ошибок с кастомными исключениями"""
    
    @app.exception_handler(BaseAPIException)
    async def api_exception_handler(request: Request, exc: BaseAPIException):
        """Обработка кастомных API исключений"""
        logger.warning(f"API Exception: {exc.detail} (code: {exc.error_code})")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                    "details": None
                }
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Обработка стандартных HTTPException (для обратной совместимости)"""
        logger.warning(f"HTTPException: {exc.detail} (status: {exc.status_code})")
        
        # Маппинг для стандартных исключений, которые еще не переведены на кастомные
        error_mapping = {
            "Not authenticated": "NOT_AUTHENTICATED",
            "Invalid token": "INVALID_TOKEN", 
            "Forbidden": "FORBIDDEN",
            "User not found": "USER_NOT_FOUND",
            "Email already registered": "EMAIL_EXISTS",
            "Invalid credentials": "INVALID_CREDENTIALS"
        }
        
        error_code = error_mapping.get(exc.detail, "HTTP_ERROR")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": error_code,
                    "message": exc.detail,
                    "details": None
                }
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Обработка ошибок валидации Pydantic"""
        logger.warning(f"Validation error: {exc.errors()}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": exc.errors()
                }
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """Обработка ошибок базы данных"""
        logger.error(f"Database error: {str(exc)}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Internal server error",
                    "details": None
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Обработка всех остальных исключений"""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR", 
                    "message": "Internal server error",
                    "details": None
                }
            }
        )