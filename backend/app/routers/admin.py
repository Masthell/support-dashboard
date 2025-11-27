from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    return {"message": "Admin dashboard"}

@router.get("/admin/users")
def admin_users(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    return {"message": "Admin users management"}