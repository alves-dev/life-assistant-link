import logging
from datetime import datetime

from app.config.setting import setting
from app.domain.zone import repository
from app.domain.zone.event import Event, Action
from app.infrastructure.broker import RabbitMQ


def launch_event(event: Event) -> bool:
    send_broker(event)

    # only add
    if event.action == Action.CAME_IN:
        repository.add_event(event)
        return True

    # if it is WENT_OUT, it validates that it CAME_IN before
    event_came_in = repository.find_event_came_in_by_went_out(event)
    if event_came_in:
        send_broker_remained(event_came_in, event)

        repository.remove_event(event_came_in)
        return True


def send_broker_remained(event_came_in: Event, event_went_out: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    event_broker = parser_event_remained(event_came_in, event_went_out)
    logging.info(event_broker)
    if event_broker.get('person_id') is None:
        logging.info(f'Person [{event_came_in.person}] not found, event will not be sent!')
        return None
    RabbitMQ().send(event_broker)


def send_broker(event: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    event_broker = parser_event(event)
    logging.info(event_broker)
    if event_broker.get('person_id') is None:
        logging.info(f'Person [{event.person}] not found, event will not be sent!')
        return None
    RabbitMQ().send(event_broker)


def parser_event(event: Event) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS.get(event.person, None),
        "datetime": transform_date(event.date),
        "action": event.action.name,
        "local": event.zone,
        "origin": "Home assistant"
    }


def parser_event_remained(event_came_in: Event, event_went_out: Event) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS.get(event_came_in.person, None),
        "datetime": transform_date(event_came_in.date),
        "action": 'REMAINED',
        "local": event_went_out.zone,
        "minutes": (event_went_out.date - event_came_in.date).seconds / 60,
        "origin": "Home assistant"
    }


def transform_date(date: datetime) -> str:
    return date.__str__().replace(' ', 'T') + '-03:00'
