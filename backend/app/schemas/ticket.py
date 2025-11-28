from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TicketStatus(str, Enum):
    """статусы"""
    OPEN = "open"
    IN_PROGRESS = "in_progress" 
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """уровни приоритета"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketCreate(BaseModel):
    """схема для создания нового тикета"""
    
    title: str = Field(..., min_length=1, max_length=200, description="Brief ticket title")
    description: str = Field(..., min_length=1, max_length=5000, description="Detailed description")
    # user_id исключен - берется из JWT токена

class TicketUpdate(BaseModel):
    """схема для обновления тикетов"""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)  
    status: Optional[TicketStatus] = Field(None, description="Ticket status")
    priority: Optional[TicketPriority] = Field(None, description="Priority level")


class TicketResponse(BaseModel):
    """Схема данных билетов в ответах API"""
    
    id: int
    title: str
    description: Optional[str]
    status: TicketStatus
    priority: TicketPriority
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True