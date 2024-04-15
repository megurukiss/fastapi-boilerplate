from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.domain.command import CreateEventCommand
from app.event.domain.entity.event import Event
from app.event.domain.usecase.event import EventUseCase
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from core.db import Transactional

class EventService(EventUseCase):
    def __init__(self, *, repository: EventRepositoryAdapter,user_repository:UserRepositoryAdapter):
        self.repository = repository
        self.user_repository = user_repository

    # @Transactional()
    async def create_event(self, *, command: CreateEventCommand) -> Event:
        event = Event.create(
            title=command.title,
            description=command.description,
            status=command.status,
            startTime=command.startTime,
            endTime=command.endTime
        )
        # event.invitees = command.invitees
        await self.repository.save(event=event)
        return event

    async def get_event_by_id(self, *, event_id: int) -> Event:
        return await self.repository.get_event_by_id(event_id=event_id)

    async def delete_event_by_id(self, *, event_id: int) -> None:
        await self.repository.delete_event_by_id(event_id=event_id)

    async def get_invitees_by_id(self, *, event_id: int) -> list[User]:
        return await self.repository.get_invitees_by_id(event_id=event_id)

    async def add_existing_invitee_by_id(self, *, event_id: int, user:User ) -> None:
        await self.repository.add_invitee_by_id(event_id=event_id, user=user)

    async def add_existing_invitee_by_userid(self, *, event_id: int, user_id:int ) -> None:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        await self.repository.add_invitee_by_id(event_id=event_id, user=user)
