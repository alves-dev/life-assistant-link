from datetime import datetime

from app.domain.zone import zone_repository as repository
from app.domain.zone.event import PersonTrackingEvent, Action


def test_repository():
    date_a = datetime.today()
    date_b = datetime.today()

    event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = PersonTrackingEvent(Action.CAME_IN, 'gym', 'maria', date_b)
    event_c = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', datetime.today())

    # Devido a outros testes, o repositório pode nao estar vazio.
    repository.clear()

    repository.add_event(event_a)
    repository.add_event(event_b)
    repository.add_event(event_c)

    assert event_a == repository.find_event_came_in_by_went_out(event_c)
    assert 3 == len(repository.get_all())

    repository.remove_event(event_b)
    assert 2 == len(repository.get_all())

    repository.clear()
    assert 0 == len(repository.get_all())
