from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.core.config import settings
from app.database import get_db, engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User  
from sqlalchemy import select  
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting FastAPI application...")
    yield
    # Shutdown
    print("Shutting down FastAPI application...")
    await engine.dispose()

app = FastAPI(
    title="Support System API",
    description="API for Support Dashboard",
    lifespan=lifespan,
    version="1.0.0"
)

# тестовый эндпоинт
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Проверка здоровья приложения"""
    try:
        await db.execute(text("SELECT 1"))
        
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
app.include_router(auth.router, prefix="/auth") 