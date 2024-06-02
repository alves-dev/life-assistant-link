from fastapi.testclient import TestClient

from app.config.setting import setting
from app.main import app

API_KEY = setting.API_KEY
client = TestClient(app)


def test_create_zone_event_201():
    zone_event_data = {
        "action": "enter",
        "zone": "living_room",
        "person": "John Doe"
    }

    response = client.post("/api/v1/zone/event", json=zone_event_data, headers={"api-key": API_KEY})
    assert 201 == response.status_code
    assert "Created" == response.json()


def test_create_zone_event_api_key_invalid():
    zone_event_data = {
        "action": "enter",
        "zone": "living_room",
        "person": "John Doe"
    }

    response = client.post("/api/v1/zone/event", json=zone_event_data,
                           headers={"api-key": "invalid api-key"})
    assert 401 == response.status_code
    assert "API Key invalid" in response.text


def test_create_zone_event_400():
    zone_event_data = {
        "action": "invalid",
        "zone": "living_room",
        "person": "John Doe"
    }

    response = client.post("/api/v1/zone/event", json=zone_event_data, headers={"api-key": API_KEY})
    assert 400 == response.status_code
    assert "Event action invalid" in response.text
