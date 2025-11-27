from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy import select, func  
from app.database import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse
from app.core.dependencies import get_current_user
from fastapi import Query

router = APIRouter()

# эндпоинт создания тикета:
@router.post("/tickets", response_model=TicketResponse)
async def create_ticket(  
    ticket_data: TicketCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    user_id = int(current_user["sub"])
    
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        user_id=user_id,
        status="open",
        priority="medium"
    )
    db.add(ticket)
    await db.commit()  
    await db.refresh(ticket)  
    return ticket

@router.get("/tickets")
async def get_tickets(  
    status: str = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=1, le=100, description="Items per page"), 
    db: AsyncSession = Depends(get_db)  
):
    
    query = select(Ticket)
    
    if status:
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

# READ ONE - один тикет по ID 
@router.get("/tickets/{ticket_id}")
async def get_ticket(  
    ticket_id: int, 
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "user_id": ticket.user_id,
        "created_at": ticket.created_at
    }

# UPDATE - обновление тикета
@router.put("/tickets/{ticket_id}")
async def update_ticket(  
    ticket_id: int, 
    title: str = None, 
    description: str = None, 
    status: str = None,
    db: AsyncSession = Depends(get_db)  
):
  
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if title is not None:
        ticket.title = title
    if description is not None:
        ticket.description = description
    if status is not None:
        ticket.status = status
    
    await db.commit()  
    await db.refresh(ticket)  
    
    return {
        "id": ticket.id,
        "title": ticket.title,
        "status": ticket.status,
        "message": "Ticket updated"
    }

# DELETE - удаление тикета 
@router.delete("/tickets/{ticket_id}")
async def delete_ticket(  
    ticket_id: int, 
    db: AsyncSession = Depends(get_db)  
):
   
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    await db.delete(ticket)  
    await db.commit() 
    
    return {"message": f"Ticket {ticket_id} deleted successfully"}

@router.get("/my-tickets")
async def get_my_tickets(  
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  
):
    user_id = int(current_user["sub"])
    
 
    result = await db.execute(select(Ticket).where(Ticket.user_id == user_id))
    tickets = result.scalars().all()
    
    return {"tickets": tickets}