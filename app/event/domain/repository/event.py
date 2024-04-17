from abc import ABC, abstractmethod
from app.event.domain.entity.event import Event
from app.user.domain.entity.user import User


class EventRepo(ABC):

    @abstractmethod
    async def get_event_by_id(self, *, event_id: int) -> Event | None:
        """Get event by id"""

    @abstractmethod
    async def save(self, *, event: Event) -> None:
        """Save event"""

    @abstractmethod
    async def delete_event_by_id(self, *, event_id: int) -> None:
        """Delete event"""

    @abstractmethod
    async def get_invitees_by_id(self, *, event_id: int) -> list[User]:
        """Get invitees by id"""

    @abstractmethod
    async def add_invitee_by_id(self, *, event_id: int, user: User) -> None:
        """Add invitee by id"""