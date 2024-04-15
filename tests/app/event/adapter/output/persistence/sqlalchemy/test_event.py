import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.domain.entity.event import Event, StatusEnum
from app.event.domain.command import CreateEventCommand
from unittest.mock import AsyncMock
from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from app.event.domain.repository.event import EventRepo
from tests.support.event_fixture import make_event


event_repo = EventSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    event = make_event()
    # When, Then
    await event_repo.save(event=event)

@pytest.mark.asyncio
async def test_get_event_by_id(session: AsyncSession):
    # Given
    event = make_event()
    await event_repo.save(event=event)

    event_id=1
    # When
    sut = await event_repo.get_event_by_id(event_id=event_id)
    # Then
    assert sut is not None
    assert sut.id == event.id

@pytest.mark.asyncio
async def test_delete_event_by_id(session: AsyncSession):
    # Given
    event = make_event()
    await event_repo.save(event=event)

    event_id=1
    # When
    sut=await event_repo.get_event_by_id(event_id=event_id)
    assert sut is not None
    await event_repo.delete_event_by_id(event_id=event_id)
    # Then
    sut = await event_repo.get_event_by_id(event_id=event_id)
    assert sut is None