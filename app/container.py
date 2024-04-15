from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.application.service.jwt import JwtService
from app.event.application.service.event import EventService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)

    jwt_service = Factory(JwtService)

    event_repo = Singleton(EventSQLAlchemyRepo)
    event_repo_adapter = Factory(EventRepositoryAdapter, event_repo=event_repo)

    user_service = Factory(UserService, repository=user_repo_adapter,event_repository=event_repo_adapter)
    event_service = Factory(EventService, repository=event_repo_adapter,user_repository=user_repo_adapter)