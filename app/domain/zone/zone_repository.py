from app.domain.zone.event import PersonTrackingEvent, Action


event_list: list[PersonTrackingEvent] = []


def add_event(event: PersonTrackingEvent):
    event_list.append(event)


def remove_event(event: PersonTrackingEvent):
    event_list.remove(event)


def find_event_came_in_by_went_out(event: PersonTrackingEvent) -> PersonTrackingEvent | None:
    for e in event_list:
        if e.person == event.person and e.zone == event.zone and e.action == Action.CAME_IN:
            return e
    return None


def get_all() -> list[PersonTrackingEvent]:
    return event_list.copy()


def clear():
    event_list.clear()
