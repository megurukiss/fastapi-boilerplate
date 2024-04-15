from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.event.adapter.input.api.v1.request import CreateEventRequest, AddInviteeRequest
from app.event.application.dto import CreateEventResponseDTO, GetEventResponseDTO,AddInviteeResponseDTO
from app.event.domain.command import CreateEventCommand
from app.event.domain.usecase.event import EventUseCase

event_router = APIRouter()

@event_router.post(
    "",
    response_model=CreateEventResponseDTO,
)
@inject
async def create_event(
        request: CreateEventRequest,
        usecase: EventUseCase = Depends(Provide[Container.event_service]),
):
    command=CreateEventCommand(**request.model_dump())
    event=await usecase.create_event(command=command)
    return {"id":event.id,"title": event.title, "description": event.description, "status": event.status,
            "startTime": event.startTime, "endTime": event.endTime}

@event_router.get(
    "/{event_id}",
    response_model=GetEventResponseDTO,
)
@inject
async def get_event_by_id(
        event_id:int,
        usecase: EventUseCase = Depends(Provide[Container.event_service]),
):
    event=await usecase.get_event_by_id(event_id=event_id)
    return {"id": event.id, "title": event.title, "description": event.description, "status": event.status,
            "startTime": event.startTime, "endTime": event.endTime, "createdAt": event.created_at, "updatedAt": event.updated_at}


@event_router.delete("/{event_id}")
@inject
async def delete_event_by_id(
        event_id:int,
        usecase: EventUseCase = Depends(Provide[Container.event_service]),
):
    await usecase.delete_event_by_id(event_id=event_id)
    return {"message": "success"}

@event_router.patch("/{event_id}",
                    response_model=AddInviteeResponseDTO)
@inject
async def add_invitee_by_id(
        request: AddInviteeRequest,
        event_id:int,
        usecase: EventUseCase = Depends(Provide[Container.event_service]),
):
    await usecase.add_existing_invitee_by_userid(event_id=event_id, user_id=request.user_id)
    return {"event_id": event_id, "user_id": request.user_id}