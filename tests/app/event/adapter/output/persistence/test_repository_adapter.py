from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.domain.repository.event import EventRepo
from tests.support.event_fixture import make_event

event_repo_mock = AsyncMock(spec=EventRepo)
repository_adapter = EventRepositoryAdapter(event_repo=event_repo_mock)

@pytest.mark.asyncio
async def test_get_events_by_id(session: AsyncSession):
    event=make_event()
    event_repo_mock.get_event_by_id.return_value=event
    repository_adapter.event_repo=event_repo_mock

    sut=await repository_adapter.get_event_by_id(event_id=event.id)
    assert sut is not None
    assert sut.title==event.title
    assert sut.description==event.description
    assert sut.status==event.status
    assert sut.startTime==event.startTime
    assert sut.endTime==event.endTime
