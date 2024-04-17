import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.session import session, session_factory
from app.event.domain.entity.event import Event
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from sqlalchemy import select
from tests.support.event_fixture import make_event
from tests.support.user_fixture import make_user
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo

event_repo = EventSQLAlchemyRepo()
user_repo = UserSQLAlchemyRepo()

@pytest.mark.asyncio
async def test_save_event_user(session: AsyncSession):
    event=make_event()
    user=make_user()
    event.invitees.append(user)
    await event_repo.save(event=event)

@pytest.mark.asyncio
async def test_save_user_event(session: AsyncSession):
    event=make_event()
    user=make_user()
    user.events.append(event)
    await user_repo.save(user=user)

@pytest.mark.asyncio
async def test_get_invitees_by_id(session: AsyncSession):
    event=make_event()
    user=make_user()
    event.invitees.append(user)
    await event_repo.save(event=event)
    await user_repo.save(user=user)
    event_id=1
    invitees=await event_repo.get_invitees_by_id(event_id=event_id)
    # print([i.id for i in invitees])

@pytest.mark.asyncio
async def test_delete_event_user_by_id(session: AsyncSession):
    event=make_event()
    user=make_user()
    event.invitees.append(user)
    await event_repo.save(event=event)
    event_id=1
    user_id=1
    await event_repo.delete_event_by_id(event_id=event_id)

    sut = await event_repo.get_event_by_id(event_id=event_id)
    assert sut is None

    sut=await user_repo.get_user_by_id(user_id=user_id)
    assert sut is not None

@pytest.mark.asyncio
async def test_add_event_to_existing_user(session: AsyncSession):
    user=make_user()
    await user_repo.save(user=user)
    user=await user_repo.get_user_by_id(user_id=1)
    events=await user_repo.get_events_by_id(user_id=1)
    assert len(events)==0
    event=make_event()
    event.invitees.append(user)
    await event_repo.save(event=event)
    events=await user_repo.get_events_by_id(user_id=1)
    assert len(events)==1
    assert events[0].id==1

@pytest.mark.asyncio
async def test_add_user_to_existing_event(session: AsyncSession):
    event=make_event()
    await event_repo.save(event=event)
    event=await event_repo.get_event_by_id(event_id=1)
    invitees=await event_repo.get_invitees_by_id(event_id=1)
    assert len(invitees)==0
    user=make_user()
    user.events.append(event)
    await user_repo.save(user=user)
    invitees=await event_repo.get_invitees_by_id(event_id=1)
    assert len(invitees)==1
    assert invitees[0].id==1

@pytest.mark.asyncio
async def test_add_existed_invitee_by_id(session: AsyncSession):
    event=make_event()
    await event_repo.save(event=event)
    user=make_user()
    await user_repo.save(user=user)

    user=await user_repo.get_user_by_id(user_id=1)
    await event_repo.add_invitee_by_id(event_id=1, user=user)
    invitees=await event_repo.get_invitees_by_id(event_id=1)
    assert len(invitees)==1
    assert invitees[0].id==1

@pytest.mark.asyncio
async def test_add_existed_event_by_id(session: AsyncSession):
    event=make_event()
    await event_repo.save(event=event)
    user=make_user()
    await user_repo.save(user=user)

    event=await event_repo.get_event_by_id(event_id=1)
    await user_repo.add_event_by_id(user_id=1, event=event)
    events=await user_repo.get_events_by_id(user_id=1)
    assert len(events)==1
    assert events[0].id==1

