from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.application.exception import EventNotFoundException
from app.event.application.service.event import EventService
from app.event.domain.command import CreateEventCommand
from app.event.domain.entity.event import EventRead, StatusEnum
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from tests.support.event_fixture import make_event
from tests.support.user_fixture import make_user

repository_mock = AsyncMock(spec=EventRepositoryAdapter)
repository_mock_user= AsyncMock(spec=UserRepositoryAdapter)
event_service = EventService(repository=repository_mock, user_repository=repository_mock_user)


repository_mock = AsyncMock(spec=EventRepositoryAdapter)
repository_mock_user= AsyncMock(spec=UserRepositoryAdapter)
user_service = EventService(repository=repository_mock,user_repository=repository_mock_user)

@pytest.mark.asyncio
async def test_save_event():

    event = make_event()
    repository_mock.save.return_value = event
    event_service.repository = repository_mock

    command=CreateEventCommand(
        title="test",
        description="test",
        status=StatusEnum.TODO,
        startTime=datetime.now(),
        endTime=datetime.now(),
    )
    sut = await event_service.create_event(command=command)



