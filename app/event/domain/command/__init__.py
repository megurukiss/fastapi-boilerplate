from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.event.domain.entity.event import StatusEnum
from app.user.domain.entity.user import User


class CreateEventCommand(BaseModel):
    title: str
    description: str
    status: StatusEnum
    startTime: datetime
    endTime: datetime

