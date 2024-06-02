import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.middleware.security import authentication
from app.domain.food import food_service as service
from app.domain.food.event import FoodLiquidEvent

router = APIRouter(prefix="/api/v1/food", tags=['Food'])


class FoodLiquidRequest(BaseModel):
    person: str
    liquid: str
    amount: int


@router.post("/liquid", status_code=201, responses={401: {"description": "Unauthorized"}})
def create_liquid_food_event(request: FoodLiquidRequest, authorized: bool = Depends(authentication)) -> str:
    """
    Receives a 'FoodLiquidRequest' and transforms it into an 'FoodLiquidEvent'
    """
    logging.info(f'Event from home assistant: {request}')

    service.launch_event(FoodLiquidEvent(request.person, request.liquid, request.amount))
    return 'Created'
