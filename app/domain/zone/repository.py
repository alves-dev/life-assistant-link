from app.domain.zone.event import Event, Action


event_list: list[Event] = []


def add_event(event: Event):
    event_list.append(event)


def remove_event(event: Event):
    event_list.remove(event)


def find_event_came_in_by_went_out(event: Event) -> Event | None:
    for e in event_list:
        if e.person == event.person and e.zone == event.zone and e.action == Action.CAME_IN:
            return e
    return None


def get_all() -> list[Event]:
    return event_list.copy()


def clear():
    event_list.clear()
