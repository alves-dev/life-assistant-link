import logging
from fastapi import HTTPException

from app.api.food.food_controller import FoodLiquidRequest
from app.config.setting import setting
from app.domain.food.event import FoodLiquidEvent, HealthNutriTrackLiquidEvent
from app.infrastructure.broker import RabbitMQ, RabbitMQV2


def launch_event(liquid: FoodLiquidRequest) -> bool:
    person_id = setting.PERSON_UUIDS.get(liquid.person, None)
    if person_id is None:
        logging.warning(f"Person '{liquid.person}' not found, event will not be sent!")
        raise HTTPException(status_code=400, detail=f"Person '{liquid.person}' not found")

    event = FoodLiquidEvent(person_id, liquid.datetime, liquid.liquid.upper(), liquid.amount)
    logging.info(event)

    _send_broker(event)
    return True


def launch_event_v2(liquid: FoodLiquidRequest) -> bool:
    event = HealthNutriTrackLiquidEvent(liquid.person, liquid.datetime, liquid.liquid, liquid.amount)
    logging.info(event)

    _send_broker_v2(event)
    return True


def _send_broker(event: FoodLiquidEvent) -> None:
    try:
        RabbitMQ().send_food(event.__dict__)
    except:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established")


def _send_broker_v2(event: HealthNutriTrackLiquidEvent) -> None:
    try:
        RabbitMQV2().send_food(event.__dict__)
    except:
        raise HTTPException(status_code=503, detail="Connection to rabbitmq not established V2")
