from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy import select, func  
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse
from app.core.dependencies import get_current_user
from app.core.exceptions import TicketNotFoundException


router = APIRouter()

# Валидные статусы для тикетов
VALID_STATUSES = ["open", "in_progress", "closed"]


@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(  
    ticket_data: TicketCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    """создать новый тикет для выбранного пользователя"""
    user_id = int(current_user["sub"])
    
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        user_id=user_id,
        status="open",
        priority="medium"
    )
    
    try:
        db.add(ticket)
        await db.commit()  
        await db.refresh(ticket)  
        return ticket
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during ticket creation")


@router.get("/tickets")
async def get_tickets(  
    status: str = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=1, le=100, description="Items per page"), 
    db: AsyncSession = Depends(get_db)  
):
    """Получите нумерованный список билетов с возможностью фильтрации по статусу"""
    query = select(Ticket)
    
    # Проверить статус фильтра
    if status:
        if status not in VALID_STATUSES:
            raise HTTPException(400, f"Invalid status. Must be one of: {VALID_STATUSES}")
        query = query.where(Ticket.status == status)
    
    skip = (page - 1) * page_size
    
    result = await db.execute(query.offset(skip).limit(page_size))
    tickets = result.scalars().all()
    
    count_result = await db.execute(select(func.count()).select_from(Ticket))
    total = count_result.scalar_one()
    
    return {
        "tickets": tickets,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size  
        }
    }


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(  
    ticket_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Получите конкретный тикет по идентификатору"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise TicketNotFoundException()
    
    return ticket


@router.put("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(  
    ticket_id: int, 
    title: str = None, 
    description: str = None, 
    status: str = None,
    db: AsyncSession = Depends(get_db)  
):
    """обновление деталей тикета"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise TicketNotFoundException()
    
    # Проверить статус
    if status and status not in VALID_STATUSES:
        raise HTTPException(400, f"Invalid status. Must be one of: {VALID_STATUSES}")
    
    # Обновление полей
    if title is not None:
        ticket.title = title
    if description is not None:
        ticket.description = description
    if status is not None:
        ticket.status = status
    
    try:
        await db.commit()  
        await db.refresh(ticket)  
        return ticket
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during ticket update")


@router.delete("/tickets/{ticket_id}")
async def delete_ticket(  
    ticket_id: int, 
    db: AsyncSession = Depends(get_db)  
):
    """Удалить билет по ID"""
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise TicketNotFoundException()
    
    try:
        await db.delete(ticket)  
        await db.commit() 
        return {"message": f"Ticket {ticket_id} deleted successfully"}
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during ticket deletion")


@router.get("/my-tickets")
async def get_my_tickets(  
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    """Получить тикеты, принадлежащие текущему пользователю"""
    user_id = int(current_user["sub"])
    
    result = await db.execute(select(Ticket).where(Ticket.user_id == user_id))
    tickets = result.scalars().all()
    
    return {"tickets": tickets}


@router.get("/operator/tickets") 
async def operator_tickets(current_user: dict = Depends(get_current_user)):
    """Конечная точка оператора — получить все системные билеты (только для администратора/оператора)."""
    if current_user.get("role") not in ["admin", "operator"]:
        raise HTTPException(403, "Operator access required")
    return {"message": "Operator tickets - все тикеты системы"}


@router.put("/operator/tickets/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: int, 
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Назначить тикет оператору (только для администратора/оператора)"""
    if current_user.get("role") not in ["admin", "operator"]:
        raise HTTPException(403, "Operator access required")
    
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise TicketNotFoundException()
    
    # Здесь можно добавить логику назначения
    # ticket.assigned_to = current_user["sub"]
    
    try:
        await db.commit()
        return {"message": f"Ticket {ticket_id} assigned to operator"}
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Database error during ticket assignment")