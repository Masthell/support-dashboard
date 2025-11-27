from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None  
    status: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True