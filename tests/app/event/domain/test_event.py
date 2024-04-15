import pytest

from app.event.domain.entity.event import Event, StatusEnum
from app.event.domain.command import CreateEventCommand
from app.user.domain.entity.user import User
from app.user.domain.command import CreateUserCommand
from app.user.application.service.user import UserService
from unittest.mock import AsyncMock
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.exception import (
    PasswordDoesNotMatchException,
)
from app.user.domain.repository.user import UserRepo
from tests.support.user_fixture import make_user


user_repo_mock = AsyncMock(spec=UserRepo)
repository_adapter = UserRepositoryAdapter(user_repo=user_repo_mock)


@pytest.mark.asyncio
async def test_create_user():
    limit = 1
    prev = 1
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.get_users.return_value = [user]
    repository_adapter.user_repo = user_repo_mock

    sut = await repository_adapter.get_users(limit=limit, prev=prev)
    result = sut[0]
    assert result.id == user.id
    print(result.events)


