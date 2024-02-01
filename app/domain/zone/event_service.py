import logging
from app.config.setting import setting
from app.domain.zone import repository
from app.domain.zone.event import Event, Action


def launch_event(event: Event) -> bool:
    send_broker(event)

    # only add
    if event.action == Action.CAME_IN:
        repository.add_event(event)
        return True

    # if it is CAME_IN, it validates that it WENT_OUT before
    event_came_in = repository.find_event_came_in_by_went_out(event)
    if event_came_in:
        send_broker_remained(event_came_in, event)

        repository.remove_event(event_came_in)
        return True


def send_broker_remained(event_came_in: Event, event_went_out: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    # TODO: aqui tenho que enviar o evento para o rabbitmq
    logging.info(parser_event_remained(event_came_in, event_went_out))
    pass


def send_broker(event: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    # TODO: aqui tenho que enviar o evento para o rabbitmq
    logging.info(parser_event(event))
    pass


def parser_event(event: Event) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS[event.person],
        "datetime": event.date.__str__().replace(' ', 'T'),
        "action": event.action.name,
        "local": event.zone,
        "origin": "Home assistant"
    }


def parser_event_remained(event_came_in: Event, event_went_out: Event) -> dict | None:
    return {
        "type": "PERSON_TRACKING",
        "person_id": setting.PERSON_UUIDS[event_came_in.person],
        "datetime": event_came_in.date.__str__().replace(' ', 'T'),
        "action": 'REMAINED',
        "local": event_went_out.zone,
        "minutes": (event_went_out.date - event_came_in.date).seconds / 60,
        "origin": "Home assistant"
    }
