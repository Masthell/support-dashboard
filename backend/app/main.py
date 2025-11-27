from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import get_db, engine


app = FastAPI(
    title="Support System API",
    description="API for Support Dashboard",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Welcome to Support Dashboard API"}

@app.get("/info")
async def info():
    """Информация  настройках"""
    return {
        "app_name": "Support Dashboard",
        "algorithm": settings.ALGORITHM,
        "token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "status": "running"
    }

@app.get("/test-db")
async def test_db():
    """Тест подключения к БД"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {
                "status": "Database connected successfully",
                "database": "MySQL",
                "test_query": "SELECT 1 - OK",
                "connection_test": True
            }
    except Exception as e:
        return {
            "status": "❌ Database connection failed",
            "error": str(e)
        }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Полная проверка здоровья приложения"""
    try:
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "environment": "development",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/api/status")
async def api_status():
    return {
        "api": "Support Dashboard API",
        "version": "1.0",
        "status": "active"
    }

@app.get("/config-test")
async def config_test():
    """Тест загрузки конфигурации (безопасный)"""
    return {
        "algorithm": settings.ALGORITHM,
        "token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "secret_key_length": len(settings.SECRET_KEY),
        "database_configured": True if settings.DATABASE_URL else False
    }


# Подключаем роутеры
from app.routers import users, tickets, auth

app.include_router(users.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")

from app.routers import users, tickets, auth  
app.include_router(users.router, prefix="/api")
app.include_router(tickets.router, prefix="/api") 
app.include_router(auth.router, prefix="/auth") 