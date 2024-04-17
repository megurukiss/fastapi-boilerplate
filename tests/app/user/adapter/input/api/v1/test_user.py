from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from app.event.domain.entity.event import StatusEnum
from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.exception import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from tests.support.event_fixture import make_event
from tests.support.token import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/user", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": 1, "email": "a@b.c", "nickname": "hide"}


@pytest.mark.asyncio
async def test_create_user_password_does_not_match(session: AsyncSession):
    # Given
    body = {
        "email": "h@id.e",
        "password1": "a",
        "password2": "b",
        "nickname": "hide",
        "lat": 37.123,
        "lng": 127.123,
    }
    exc = PasswordDoesNotMatchException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user_duplicated_user(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    body = {
        "email": "a@b.c",
        "password1": "a",
        "password2": "a",
        "nickname": "hide",
        "lat": 37.123,
        "lng": 127.123,
    }
    exc = DuplicateEmailOrNicknameException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    email = "h@id.e"
    nickname = "hide"
    body = {
        "email": email,
        "password1": "a",
        "password2": "a",
        "nickname": nickname,
        "lat": 37.123,
        "lng": 127.123,
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {"email": email, "nickname": nickname}

    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_email_or_nickname(nickname=nickname, email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    email = "h@id.e"
    password = "password"
    body = {"email": email, "password": password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given
    email = "h@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    body = {"email": email, "password": password}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    sut = response.json()
    assert "token" in sut
    assert "refresh_token" in sut


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    email = "h@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    event=make_event()
    session.add(event)
    await session.commit()

    #
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/event/1/invitee", headers=HEADERS, json={"user_id": 1})

    assert response.json() == {"event_id": 1, "user_id": 1}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/user/1", headers=HEADERS)

    sut = response.json()
    assert sut["id"] == 1
    assert sut["email"] == email
    assert sut["nickname"] == "hide"
    assert len(sut["events"]) == 1
    assert sut["events"][0]=="title: title"

@pytest.mark.asyncio
async def test_add_event_by_id(session: AsyncSession):
    email = "h@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    event=make_event()
    session.add(event)
    await session.commit()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 1})

    assert response.json() == {"user_id": 1, "event_id": 1}
    user_repo = UserSQLAlchemyRepo()
    events = await user_repo.get_events_by_id(user_id=1)
    assert events is not None
    assert events[0].id == 1
    assert events[0].title == "title"

@pytest.mark.asyncio
async def test_merge_events_by_id(session: AsyncSession):
    # 1 user 3 event case
    email = "h@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # overlapping event1 and event2
    event1=make_event(title="title1",description="description1",status=StatusEnum.TODO,
                      startTime=datetime(2024, 4, 10, 9, 0),
                      endTime=datetime(2024, 4, 10, 10, 0))
    session.add(event1)
    await session.commit()

    event2=make_event(title="title2",description="description2",status=StatusEnum.TODO,
                      startTime=datetime(2024, 4, 10, 10, 0),
                      endTime=datetime(2024, 4, 10, 11, 0))
    session.add(event2)
    await session.commit()

    # non-overlapping event3
    event3=make_event(title="title3",description="description3",status=StatusEnum.TODO,
                        startTime=datetime(2024, 4, 10, 12, 0),
                        endTime=datetime(2024, 4, 10, 13, 0))
    session.add(event3)
    await session.commit()

    user_repo = UserSQLAlchemyRepo()
    event_repo = EventSQLAlchemyRepo()

    # add events to user
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 1})
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 2})
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 3})

    # merge events
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/events", headers=HEADERS)

    assert response.json() =={"message": "success"}

    event=await event_repo.get_event_by_id(event_id=1)
    assert event is None

    event=await event_repo.get_event_by_id(event_id=2)
    assert event is None

    event=await event_repo.get_event_by_id(event_id=3)
    assert event is not None

    new_event=await event_repo.get_event_by_id(event_id=4)
    assert new_event is not None
    assert new_event.title == "title1;title2"
    assert new_event.description == "title1: description1;title2: description2"

    events = await user_repo.get_events_by_id(user_id=1)
    assert len(events)==2
    assert events[0].id == 3
    assert events[0].title == "title3"
    assert events[0].description == "description3"

    assert events[1].id == 4
    assert events[1].title == "title1;title2"
    assert events[1].description == "title1: description1;title2: description2"

@pytest.mark.asyncio
async def test_merge_events_by_id_2(session: AsyncSession):
    # 2 user 2 event case
    email = "h@id.e"
    password = "password"
    user = make_user(
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    email = "hhh@id.e"
    password = "password"
    user = make_user(
        password=password,
        email=email,
        nickname="hide2",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # overlapping event1 and event2
    event1=make_event(title="title1",description="description1",status=StatusEnum.TODO,
                      startTime=datetime(2024, 4, 10, 9, 0),
                      endTime=datetime(2024, 4, 10, 10, 0))
    session.add(event1)
    await session.commit()

    event2=make_event(title="title2",description="description2",status=StatusEnum.TODO,
                      startTime=datetime(2024, 4, 10, 10, 0),
                      endTime=datetime(2024, 4, 10, 11, 0))
    session.add(event2)
    await session.commit()


    user_repo = UserSQLAlchemyRepo()
    event_repo = EventSQLAlchemyRepo()

    # add event1 to user1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 1})
    # add event2 to user1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/event", headers=HEADERS, json={"event_id": 2})

    # add event2 to user2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/2/event", headers=HEADERS, json={"event_id": 2})

    # merge events
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/user/1/events", headers=HEADERS)

    assert response.json() =={"message": "success"}

    event=await event_repo.get_event_by_id(event_id=1)
    assert event is None

    event=await event_repo.get_event_by_id(event_id=2)
    assert event is None

    new_event=await event_repo.get_event_by_id(event_id=3)
    assert new_event is not None
    assert new_event.title == "title1;title2"
    assert new_event.description == "title1: description1;title2: description2"

    new_invitees=await event_repo.get_invitees_by_id(event_id=3)
    assert len(new_invitees)==2
    assert new_invitees[0].id==1
    assert new_invitees[1].id==2

    events = await user_repo.get_events_by_id(user_id=1)
    assert len(events)==1

    assert events[0].id == 3
    assert events[0].title == "title1;title2"
    assert events[0].description == "title1: description1;title2: description2"