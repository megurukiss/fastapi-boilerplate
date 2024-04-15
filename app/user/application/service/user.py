from typing import List

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.adapter.output.persistence.sqlalchemy.event import EventSQLAlchemyRepo
from app.event.domain.entity.event import Event, StatusEnum
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from app.user.domain.vo.location import Location
from core.db import Transactional
from core.helpers.token import TokenHelper

class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepositoryAdapter, event_repository:EventRepositoryAdapter):
        self.repository = repository
        self.event_repository = event_repository
    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    @Transactional()
    async def create_user(self, *, command: CreateUserCommand) -> None:
        if command.password1 != command.password2:
            raise PasswordDoesNotMatchException

        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            email=command.email,
            password=command.password1,
            nickname=command.nickname,
            location=Location(lat=command.lat, lng=command.lng),
        )
        await self.repository.save(user=user)

    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_and_password(
            email=email,
            password=password,
        )
        if not user:
            raise UserNotFoundException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def get_events_by_id(self, *, user_id: int) -> List[Event]:
        return await self.repository.get_events_by_id(user_id=user_id)

    async def add_existing_event_by_id(self, *, user_id: int, event: Event) -> None:
        await self.repository.add_event_by_id(user_id=user_id, event=event)

    async def add_existing_event_by_eventid(self, *, user_id: int, event_id: int) -> None:
        event=await self.event_repository.get_event_by_id(event_id=event_id)
        await self.repository.add_event_by_id(user_id=user_id, event=event)

    async def get_user_by_id(self, *, user_id: int) -> User:
        return await self.repository.get_user_by_id(user_id=user_id)

    async def merge_events_by_id(self, *, user_id: int) -> None:
        user=await self.repository.get_user_by_id(user_id=user_id)
        events=user.events

        #sort events by start time
        events.sort(key=lambda x: x.startTime)

        non_overlap_events=[]
        temp_events=[]
        for event in events:
            if len(temp_events)==0:
                temp_events.append(event)
            else:
                if temp_events[-1].endTime<event.startTime:
                    non_overlap_events.append(temp_events)
                    temp_events=[]
                temp_events.append(event)
        if len(temp_events)>0:
            non_overlap_events.append(temp_events)

        for temp_events in non_overlap_events:
            #skip if there is only one event
            if len(temp_events)==1:
                continue

            #do merge
            titles=[]
            description=[]
            status=[]

            for event in temp_events:
                titles.append(event.title)
                description.append(event.title+": "+event.description)
                status.append(event.status)
                await self.event_repository.delete_event_by_id(event_id=event.id)

            new_title=";".join(titles)
            new_description=";".join(description)
            if status[0]==StatusEnum.TODO:
                new_status=StatusEnum.TODO
            elif status[-1]==StatusEnum.COMPLETED:
                new_status=StatusEnum.COMPLETED
            else:
                new_status=StatusEnum.IN_PROGRESS
            new_startTime=temp_events[0].startTime
            new_endTime=temp_events[-1].endTime
            new_event=Event.create(
                title=new_title,
                description=new_description,
                status=new_status,
                startTime=new_startTime,
                endTime=new_endTime,
            )

            await self.event_repository.save(event=new_event)
            await self.add_existing_event_by_eventid(user_id=user_id, event_id=new_event.id)
        return



