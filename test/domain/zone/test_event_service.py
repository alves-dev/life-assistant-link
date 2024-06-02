from datetime import datetime, timedelta

from app.domain.zone import zone_service as service
from app.domain.zone.event import PersonTrackingEvent, Action


def test_launch_event():
    date_a = datetime.today() - timedelta(hours=1)
    date_b = datetime.today()

    event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', date_b)

    assert service.launch_event(event_a)
    assert service.launch_event(event_b)


def test_send_broker():
    date_a = datetime.today() - timedelta(hours=1)
    date_b = datetime.today()

    event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', date_b)

    service._send_broker(event_a)
    service._send_broker_remained(event_a, event_b)


def test_parser_event():
    date = datetime.today()
    event = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date)
    result = service._parser_event(event)

    expected = {
        "type": "PERSON_TRACKING",
        "person_id": None,
        "datetime": date.__str__().replace(' ', 'T') + '-03:00',
        "action": "CAME_IN",
        "local": "house",
        "origin": "Home assistant"
    }
    assert expected == result


def test_parser_event_remained():
    date_a = datetime.today() - timedelta(hours=1)
    date_b = datetime.today()

    event_a = PersonTrackingEvent(Action.CAME_IN, 'house', 'joao', date_a)
    event_b = PersonTrackingEvent(Action.WENT_OUT, 'house', 'joao', date_b)

    result = service._parser_event_remained(event_a, event_b)

    expected = {
        "type": "PERSON_TRACKING",
        "person_id": None,
        "datetime": date_a.__str__().replace(' ', 'T') + '-03:00',
        "action": "REMAINED",
        "local": "house",
        "minutes": 60,
        "origin": "Home assistant"
    }
    assert expected == result


def test_transform_date():
    date = datetime.today() - timedelta(hours=1)

    date_str = service._transform_date(date)
    date_result = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f-03:00')
    assert date == date_result
