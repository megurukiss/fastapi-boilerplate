from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from tests.support.token import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user
from tests.support.event_fixture import make_event
from app.event.domain.entity.event import StatusEnum

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_create_event(session: AsyncSession):
    body={
        "title": "title",
        "description": "description",
        "status": StatusEnum.TODO.value,
        "startTime": datetime.now().isoformat(),
        "endTime": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/event", headers=HEADERS, json=body)

    response_body = response.json()
    assert response_body["title"] == "title"
    assert response_body["description"] == "description"
    assert response_body["id"] == 1

    event_repo = EventSQLAlchemyRepo()
    event = await event_repo.get_event_by_id(event_id=1)
    assert event is not None
    assert event.id == 1
    assert event.title == "title"
    assert event.description == "description"
    assert event.status == StatusEnum.TODO

@pytest.mark.asyncio
async def test_get_event_by_id(session: AsyncSession):
    body={
        "title": "title",
        "description": "description",
        "status": StatusEnum.TODO.value,
        "startTime": datetime.now().isoformat(),
        "endTime": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/event", headers=HEADERS, json=body)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/event/1", headers=HEADERS)

    sut = response.json()
    assert sut["id"] == 1
    assert sut["title"] == "title"
    assert sut["description"] == "description"
    assert sut["status"] == StatusEnum.TODO.value

@pytest.mark.asyncio
async def test_delete_event_by_id(session: AsyncSession):
    body={
        "title": "title",
        "description": "description",
        "status": StatusEnum.TODO.value,
        "startTime": datetime.now().isoformat(),
        "endTime": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/event", headers=HEADERS, json=body)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/v1/event/1", headers=HEADERS)

    assert response.json() == {"message": "success"}
    event_repo = EventSQLAlchemyRepo()
    event = await event_repo.get_event_by_id(event_id=1)
    assert event is None


@pytest.mark.asyncio
async def test_add_invitee_by_id(session: AsyncSession):
    body={
        "title": "title",
        "description": "description",
        "status": StatusEnum.TODO.value,
        "startTime": datetime.now().isoformat(),
        "endTime": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/event", headers=HEADERS, json=body)

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
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch("/api/v1/event/1", headers=HEADERS, json={"user_id": 1})

    assert response.json() == {"event_id": 1, "user_id": 1}
    event_repo = EventSQLAlchemyRepo()
    invitees = await event_repo.get_invitees_by_id(event_id=1)
    assert invitees is not None
    assert invitees[0].id == 1


