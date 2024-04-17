from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from app.event.application.service.event import EventService
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo


class EventContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    event_sqlalchemy_repo = Singleton(EventSQLAlchemyRepo)
    event_repository_adapter = Factory(
        EventRepositoryAdapter,
        event_repo=event_sqlalchemy_repo,
    )

    event_service = Factory(EventService, repository=event_repository_adapter)
