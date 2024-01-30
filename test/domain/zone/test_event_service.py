from app.domain.zone.event import Event, Action
from app.domain.zone import event_service as service
from datetime import datetime, timedelta


def test_repository():
    date_a = datetime.today() - timedelta(hours=1)
    date_b = datetime.today()

    event_a = Event(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = Event(Action.WENT_OUT, 'house', 'joao', date_b)

    assert service.launch_event(event_a)
    assert service.launch_event(event_b)
