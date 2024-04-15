from typing import List

from sqlalchemy.orm import selectinload

from app.user.domain.entity.user import User
from core.db.session import session, session_factory
from core.db import Transactional
from app.event.domain.repository.event import EventRepo
from app.event.domain.entity.event import Event, EventRead
from sqlalchemy import select



class EventSQLAlchemyRepo(EventRepo):
    async def get_event_by_id(self, *, event_id: int) -> Event | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(Event).where(Event.id == event_id))
            return stmt.scalars().first()

    @Transactional()
    async def save(self, *, event: Event) -> None:
        session.add(event)

    async def delete_event_by_id(self, *, event_id: int) -> None:
        # await session.delete(event) if event else None
        async with session_factory() as write_session:
            user_to_delete = await self.get_event_by_id(event_id=event_id)
            if user_to_delete:
                await write_session.delete(user_to_delete)
                await write_session.commit()

    async def get_invitees_by_id(self, *, event_id: int) -> List[User]:
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(Event).options(selectinload(Event.invitees)).where(Event.id == event_id))
            event = stmt.scalars().first()
            return event.invitees

    async def add_invitee_by_id(self, *, event_id: int, user: User) -> None:
        async with session_factory() as write_session:
            stmt = await write_session.execute(select(Event).options(selectinload(Event.invitees)).where(Event.id == event_id))
            event = stmt.scalars().first()
            event.invitees.append(user)
            await write_session.commit()