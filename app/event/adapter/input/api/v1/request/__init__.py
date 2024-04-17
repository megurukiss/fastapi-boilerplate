from datetime import datetime

from pydantic import BaseModel, Field

from app.event.domain.entity.event import StatusEnum


class CreateEventRequest(BaseModel):
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    status: StatusEnum = Field(..., description="Status")
    startTime: datetime = Field(..., description="Start Time")
    endTime: datetime = Field(..., description="End Time")

class AddInviteeRequest(BaseModel):
    user_id: int = Field(..., description="User ID")