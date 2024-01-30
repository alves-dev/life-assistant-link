from app.domain.zone.event import Event, Action
from app.domain.zone import repository


def launch_event(event: Event) -> bool:
    send_broker(event)

    # only add
    if event.action == Action.CAME_IN:
        repository.add_event(event)
        return True

    # if it is CAME_IN, it validates that it WENT_OUT before
    event_came_in = repository.find_event_came_in_by_went_out(event)
    if event_came_in:
        print(event_came_in.date)
        print(event.date)
        print(event.date - event_came_in.date)

        send_broker_remained(event_came_in, event)

        repository.remove_event(event_came_in)
        return True


def send_broker_remained(event_came_in: Event, event_went_out: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    # TODO: aqui tenho que enviar o evento para o rabbitmq
    print(f'Send {event_came_in}')
    pass


def send_broker(event: Event):
    # https://github.com/alves-dev/life/blob/main/events/README.md#person_tracking
    # TODO: aqui tenho que enviar o evento para o rabbitmq
    print(f'Send {event}')
    pass