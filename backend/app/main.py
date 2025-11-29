from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.core.config import settings
from app.database import get_db, engine
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.core.error_handlers import setup_exception_handlers
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Управление событиями запуска и выключения приложений
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI application...")
    yield
    print("Shutting down FastAPI application...")
    await engine.dispose()

app = FastAPI(
    title="Support System API",
    description="API for Support Dashboard",
    lifespan=lifespan,
    version="1.0.0"
)

# Настройка глобальной обработки исключений
setup_exception_handlers(app)



# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# тестовый эндпоинт
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Проверка здоровья приложения"""
    try:
        await db.execute(text("SELECT 1")) # Тестовый запрос для проверки БД
        
        return {
            "status": "healthy",
            "database": "connected",
            "environment": "development",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Корневая точка с приветственным сообщением
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
        "database_configured": bool(settings.DATABASE_URL),
    }


# Подключаем роутеры
from app.routers import users, tickets, auth, admin

app.include_router(users.router, prefix="/api")
app.include_router(tickets.router, prefix="/api")
app.include_router(auth.router, prefix="/auth") 
app.include_router(admin.router, prefix="/api")