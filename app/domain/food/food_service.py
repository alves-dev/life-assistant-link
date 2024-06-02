import logging
from datetime import datetime

from fastapi import HTTPException

from app.config.setting import setting
from app.domain.food.event import FoodLiquidEvent
from app.infrastructure.broker import RabbitMQ


def launch_event(event: FoodLiquidEvent) -> bool:
    _send_broker(event)
    return True


def _send_broker(event: FoodLiquidEvent):
    # https://github.com/alves-dev/life/tree/main/events#alimenta%C3%A7%C3%A3o-routing_key---food-1
    event_broker = _parser_liquid_event(event)
    logging.info(event_broker)
    if event_broker.get('person_id') is None:
        logging.info(f'Person [{event.person}] not found, event will not be sent!')
        return None

    try:
        RabbitMQ().send_food(event_broker)
    except:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established")


def _parser_liquid_event(event: FoodLiquidEvent) -> dict | None:
    return {
        "type": "LIQUID_FOOD",
        "person_id": setting.PERSON_UUIDS.get(event.person, None),
        "datetime": _get_date(),
        "liquid": event.liquid,
        "amount": event.amount
    }


def _get_date() -> str:
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M")

    return formatted_date + '-03:00'
