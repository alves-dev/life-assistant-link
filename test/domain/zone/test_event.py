from app.domain.zone.event import PersonTrackingEvent, Action
from datetime import datetime


def test_create_event():
    date_a = datetime.today()
    date_b = datetime.today()

    event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = PersonTrackingEvent(Action.CAME_IN, 'gym', 'maria', date_b)
    event_c = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', datetime.today())

    assert event_a.action == Action.CAME_IN
    assert event_a.zone == 'house'
    assert event_a.person == 'joao'
    assert event_a.date == date_a

    assert event_b.action == Action.CAME_IN
    assert event_b.zone == 'gym'
    assert event_b.person == 'maria'
    assert event_b.date == date_b

    assert event_c.action == Action.WENT_OUT
    assert event_c.zone == 'house'
    assert event_c.person == 'joao'
    assert event_c.date != datetime.today()
