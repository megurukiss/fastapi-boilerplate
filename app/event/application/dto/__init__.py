from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.event.domain.entity.event import StatusEnum
from app.user.domain.entity.user import User


class CreateEventResponseDTO(BaseModel):
    id: int = Field(..., description="Event ID")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    status: StatusEnum = Field(..., description="Status")
    startTime: datetime = Field(..., description="Start Time")
    endTime: datetime = Field(..., description="End Time")

class GetEventResponseDTO(BaseModel):
    id: int = Field(..., description="Event ID")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    status: StatusEnum = Field(..., description="Status")
    startTime: datetime = Field(..., description="Start Time")
    endTime: datetime = Field(..., description="End Time")
    createdAt: datetime = Field(..., description="Created At")
    updatedAt: datetime = Field(..., description="Updated At")
    invitees:list= Field(..., description="Invitees")

class AddInviteeResponseDTO(BaseModel):
    event_id: int = Field(..., description="Event ID")
    user_id: int = Field(..., description="User ID")