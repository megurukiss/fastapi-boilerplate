from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.event.application.dto import GetEventResponseDTO
from app.user.adapter.input.api.v1.request import CreateUserRequest, LoginRequest, AddEventRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import CreateUserResponseDTO, GetUserListResponseDTO, GetUserResponseDTO, \
    AddEventResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import IsAdmin, PermissionDependency

user_router = APIRouter()


@user_router.get(
    "",
    response_model=list[GetUserListResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
@inject
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    return await usecase.get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
@inject
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    command = CreateUserCommand(**request.model_dump())
    await usecase.create_user(command=command)
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
@inject
async def login(
    request: LoginRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    token = await usecase.login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}

@user_router.get(
    "/{user_id}",
    response_model=GetUserResponseDTO
)
@inject
async def get_user_by_id(
    user_id:int,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    user=await usecase.get_user_by_id(user_id=user_id)
    events=[]
    for event in user.events:
        events.append({"title: "+event.title})
    return {"id": user.id, "email": user.email, "nickname": user.nickname,"events": events}


@user_router.patch("/{user_id}",
                    response_model=AddEventResponseDTO)
@inject
async def add_event_by_id(
    request: AddEventRequest,
    user_id:int,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    await usecase.add_existing_event_by_eventid(user_id=user_id, event_id=request.event_id)
    return {"user_id": user_id, "event_id": request.event_id}

@user_router.patch("/{user_id}/events")
@inject
async def merge_events_by_id(
    user_id:int,
    usecase: UserUseCase = Depends(Provide[Container.user_service]),
):
    await usecase.merge_events_by_id(user_id=user_id)
    return {"message": "success"}


