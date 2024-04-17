from abc import ABC, abstractmethod
from app.user.domain.entity.user import User
from app.event.domain.command import CreateEventCommand
from app.event.domain.entity.event import Event

class EventUseCase(ABC):

    @abstractmethod
    async def create_event(self, *, command: CreateEventCommand) -> Event:
        """Create Event"""

    @abstractmethod
    async def get_event_by_id(self, *, event_id: int) -> Event:
        """Get event by id"""

    @abstractmethod
    async def delete_event_by_id(self, *, event_id: int) -> None:
        """Delete event by id"""

    @abstractmethod
    async def get_invitees_by_id(self, *, event_id: int) -> list[User]:
        """Get event invitiees"""

    @abstractmethod
    async def add_existing_invitee_by_id(self, *, event_id: int, user:User) -> None:
        """Add existing user as invitee"""

    @abstractmethod
    async def add_existing_invitee_by_userid(self, *, event_id: int, user_id:int ) -> None:
        """Add existing user as invitee by user id"""