import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.middleware.security import authentication
from app.domain.zone import zone_service as service
from app.domain.zone.event import PersonTrackingEvent, Action

router = APIRouter(prefix="/api/v1/zone", tags=['Zone'])


class ZoneEventRequest(BaseModel):
    zone: str
    person: str
    action: str


@router.post("/event", status_code=201, responses={401: {"description": "Unauthorized"}})
def create_zone_event(request: ZoneEventRequest, authorized: bool = Depends(authentication)) -> str:
    """
    Receives a 'ZoneEventRequest' and transforms it into an 'PersonTrackingEvent'
    """
    logging.info(f'Event from home assistant: {request}')

    if request.action == 'enter':
        service.launch_event(PersonTrackingEvent(Action.CAME_IN, request.zone, request.person, datetime.now()))
    elif request.action == 'leave':
        service.launch_event(PersonTrackingEvent(Action.WENT_OUT, request.zone, request.person, datetime.now()))
    else:
        raise HTTPException(status_code=400, detail="Event action invalid")

    return 'Created'
