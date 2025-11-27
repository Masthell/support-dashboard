from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse
from app.core.dependencies import get_current_user

router = APIRouter()

# эндпоинт создания тикета:
@router.post("/tickets", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,  # данные из JSON тела
    current_user: dict = Depends(get_current_user),  # зависимость
    db: Session = Depends(get_db)
):
    # User ID теперь из токена, а не из запроса
    user_id = int(current_user["sub"])
    
    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        user_id=user_id,  # ← из токена, а не из ticket_data!
        status="open",
        priority="medium"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return {"tickets": tickets}

# READ ONE - один тикет по ID 
@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
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
def update_ticket(
    ticket_id: int, 
    title: str = None, 
    description: str = None, 
    status: str = None,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Обновляем только переданные поля
    if title is not None:
        ticket.title = title
    if description is not None:
        ticket.description = description
    if status is not None:
        ticket.status = status
    
    db.commit()
    db.refresh(ticket)
    return {
        "id": ticket.id,
        "title": ticket.title,
        "status": ticket.status,
        "message": "Ticket updated"
    }

# DELETE - удаление тикета 
@router.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    return {"message": f"Ticket {ticket_id} deleted successfully"}

@router.get("/my-tickets")
def get_my_tickets(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user["sub"])
    tickets = db.query(Ticket).filter(Ticket.user_id == user_id).all()
    return {"tickets": tickets}