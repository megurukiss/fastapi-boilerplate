from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String,Enum,Column,Table,Integer,ForeignKey,DateTime
from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime
import enum
from core.db import Base
from core.db.mixins import TimestampMixin
from typing import List

class StatusEnum(enum.Enum):
    TODO="TODO"
    IN_PROGRESS="IN_PROGRESS"
    COMPLETED="COMPLETED"

# association table for many-to-many relationship between event and user
assosition_table = Table('event_user', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id', ondelete="CASCADE")),
    Column('user_id', Integer, ForeignKey('user.id', ondelete="CASCADE"))
)

class Event(Base,TimestampMixin):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False)
    startTime: Mapped[datetime]= mapped_column(DateTime)
    endTime: Mapped[datetime]= mapped_column(DateTime)
    invitees= relationship("User",secondary=assosition_table,back_populates="events")

    @classmethod
    def create(
        cls, *, title: str, description: str, status: StatusEnum, startTime: datetime, endTime: datetime
    ) -> "Event":
        return cls(
            title=title,
            description=description,
            status=status,
            startTime=startTime,
            endTime=endTime
        )

class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="EVENT ID")
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    status: StatusEnum = Field(..., title="Status")
    startTime: datetime = Field(..., title="Start Time")
    endTime: datetime = Field(..., title="End Time")
    createdAt: datetime = Field(..., title="Created At")
    updatedAt: datetime = Field(..., title="Updated At")
    invitees: list = Field(..., title="Invitees")

# class User(Base):
#     __tablename__ = "user"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(255))
#     events: Mapped[List[Event]]= relationship(secondary=assosition_table,back_populates="invitees")