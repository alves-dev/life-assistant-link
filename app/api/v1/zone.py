import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.domain.zone import event_service as service
from app.domain.zone.event import Event, Action
from app.core.middleware.security import authentication

zone_event = APIRouter()


class ZoneEvent(BaseModel):
    zone: str
    person: str
    action: str


@zone_event.post("/zone-event", status_code=201, responses={401: {"description": "Unauthorized"}})
def create_zone_event(event: ZoneEvent, authorized: bool = Depends(authentication)) -> str:
    """
    Recebe um 'ZoneEvent' e lança um 'Event'
    """
    logging.info(f'Event from home assistant: {event}')

    if event.action == 'enter':
        service.launch_event(Event(Action.CAME_IN, event.zone, event.person, datetime.now()))
    elif event.action == 'leave':
        service.launch_event(Event(Action.WENT_OUT, event.zone, event.person, datetime.now()))
    else:
        raise HTTPException(status_code=400, detail="Event action invalid")

    return 'Created'
