from datetime import datetime

from app.event.domain.entity.event import Event, StatusEnum

def make_event(
    id: int | None = None,
    title: str = "title",
    description: str = "description",
    status: StatusEnum = StatusEnum.TODO,
    startTime: datetime = datetime.now(),
    endTime: datetime = datetime.now(),
):
    return Event(
        id=id,
        title=title,
        description=description,
        status=status,
        startTime=startTime,
        endTime=endTime
    )