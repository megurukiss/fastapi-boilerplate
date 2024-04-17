from abc import ABC, abstractmethod
from typing import List

from app.event.domain.entity.event import Event
from app.user.application.dto import LoginResponseDTO
from app.user.domain.entity.user import User
from app.user.domain.command import CreateUserCommand


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def create_user(self, *, command: CreateUserCommand) -> None:
        """Create User"""

    @abstractmethod
    async def is_admin(self, *, user_id: int) -> bool:
        """Is admin"""

    @abstractmethod
    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        """Login"""

    @abstractmethod
    async def add_existing_event_by_id(self, *, user_id: int, event: Event) -> None:
        """Add existing event by id"""

    @abstractmethod
    async def add_existing_event_by_eventid(self, *, user_id: int, event_id: int) -> None:
        """Add existing event by event id"""

    @abstractmethod
    async def get_events_by_id(self, *, user_id: int) -> List[Event]:
        """Get events by id"""

    @abstractmethod
    async def get_user_by_id(self, *, user_id: int) -> User:
        """Get user by id"""

    @abstractmethod
    async def merge_events_by_id(self, *, user_id: int) -> None:
        """Merge events by id"""