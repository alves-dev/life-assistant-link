import logging
from datetime import datetime

from fastapi import HTTPException

from app.config.setting import setting
from app.domain.zone import zone_repository as repository
from app.domain.zone.event import PersonTrackingEvent, Action
from app.infrastructure.broker import RabbitMQ


def launch_event(event: PersonTrackingEvent) -> bool:
    _send_broker(event)

    # only add
    if event.action == Action.CAME_IN:
        repository.add_event(event)
        return True

    # if it is WENT_OUT, it validates that it CAME_IN before
    event_came_in = repository.find_event_came_in_by_went_out(event)
    if event_came_in:
        _send_broker_remained(event_came_in, event)

        repository.remove_event(event_came_in)
        return True


def _send_broker_remained(event_came_in: PersonTrackingEvent, event_went_out: PersonTrackingEvent):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    event_broker = _parser_event_remained(event_came_in, event_went_out)
    logging.info(event_broker)
    if event_broker.get('person_id') is None:
        logging.info(f'Person [{event_came_in.person}] not found, event will not be sent!')
        return None

    try:
        RabbitMQ().send_tracking(event_broker)
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established")


def _send_broker(event: PersonTrackingEvent):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    event_broker = _parser_event(event)
    logging.info(event_broker)
    if event_broker.get('person_id') is None:
        logging.info(f'Person [{event.person}] not found, event will not be sent!')
        return None

    try:
        RabbitMQ().send_tracking(event_broker)
    except:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established")


def _parser_event(event: PersonTrackingEvent) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS.get(event.person, None),
        "datetime": _transform_date(event.date),
        "action": event.action.name,
        "local": event.zone,
        "origin": "Home assistant"
    }


def _parser_event_remained(event_came_in: PersonTrackingEvent, event_went_out: PersonTrackingEvent) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS.get(event_came_in.person, None),
        "datetime": _transform_date(event_came_in.date),
        "action": 'REMAINED',
        "local": event_went_out.zone,
        "minutes": (event_went_out.date - event_came_in.date).seconds / 60,
        "origin": "Home assistant"
    }


def _transform_date(date: datetime) -> str:
    return date.__str__().replace(' ', 'T') + '-03:00'
