from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user


router = APIRouter()


async def require_admin(current_user: dict) -> None:
    """проверить, что текущий пользователь имеет роль администратора."""
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")


@router.get("/admin/monitoring")
async def admin_dashboard(current_user: dict = Depends(get_current_user)):
    """Панель администратора с обзором системы."""
    await require_admin(current_user)
    
    return {
        "message": "Admin dashboard",
        "stats": {
            "total_users": 150,
            "active_tickets": 23,
            "resolved_this_week": 45
        }
    }


@router.get("/admin/users")
async def admin_users(current_user: dict = Depends(get_current_user)):
    """Интерфейс управления пользователями для администраторов."""
    await require_admin(current_user)
    
    return {
        "message": "Admin users management",
        "actions": [
            "view_all_users",
            "modify_roles", 
            "reset_passwords",
            "deactivate_accounts"
        ]
    }


@router.get("/admin/system")
async def admin_system(current_user: dict = Depends(get_current_user)):
    """Администрирование и настройка системы."""
    await require_admin(current_user)
    
    return {
        "message": "System administration",
        "features": [
            "database_management",
            "backup_restore",
            "system_logs",
            "performance_metrics"
        ]
    }