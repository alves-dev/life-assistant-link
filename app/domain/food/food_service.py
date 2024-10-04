import logging

from fastapi import HTTPException

from app.api.food.food_controller import FoodLiquidRequest
from app.config.setting import setting
from app.domain.food.event import FoodLiquidEvent
from app.infrastructure.broker import RabbitMQ


def launch_event(liquid: FoodLiquidRequest) -> bool:
    person_id = setting.PERSON_UUIDS.get(liquid.person, None)
    if person_id is None:
        logging.warning(f"Person '{liquid.person}' not found, event will not be sent!")
        raise HTTPException(status_code=400, detail=f"Person '{liquid.person}' not found")

    event = FoodLiquidEvent(person_id, liquid.datetime, liquid.liquid.upper(), liquid.amount)
    logging.info(event)

    _send_broker(event)
    return True


def _send_broker(event: FoodLiquidEvent) -> None:
    try:
        RabbitMQ().send_food(event.__dict__)
    except:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established")
