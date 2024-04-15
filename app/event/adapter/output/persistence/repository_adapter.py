from app.event.domain.entity.event import Event, EventRead
from app.event.domain.repository.event import EventRepo
from app.user.domain.entity.user import User


class EventRepositoryAdapter:
    def __init__(self, *, event_repo: EventRepo):
        self.event_repo = event_repo

    async def get_event_by_id(self, *, event_id: int) -> Event | None:
        return await self.event_repo.get_event_by_id(event_id=event_id)

    async def save(self, *, event: Event) -> Event:
        await self.event_repo.save(event=event)
        return event

    async def delete_event_by_id(self, *, event_id: int) -> None:
        await self.event_repo.delete_event_by_id(event_id=event_id)

    async def get_invitees_by_id(self, *, event_id: int) -> list[User]:
        return await self.event_repo.get_invitees_by_id(event_id=event_id)

    async def add_invitee_by_id(self, *, event_id: int, user: User) -> None:
        await self.event_repo.add_invitee_by_id(event_id=event_id, user=user)