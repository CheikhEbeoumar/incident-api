from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import StatusEnum, SourceEnum

class IncidentBase(BaseModel):
    description: str
    source: SourceEnum

class IncidentCreate(IncidentBase):
    status: StatusEnum = StatusEnum.OPEN

class IncidentUpdate(BaseModel):
    status: StatusEnum

class IncidentResponse(IncidentBase):
    id: int
    status: StatusEnum
    created_at: datetime
    
    class Config:
        from_attributes = True