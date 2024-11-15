import logging
from fastapi import APIRouter, Depends
from app.api.food.requests import FoodLiquidRequest
from app.core.middleware.security import authentication
from app.domain.food import food_service as service

router = APIRouter(prefix="/api/v1/food", tags=['Food'])
router_v2 = APIRouter(prefix="/api/v2/food", tags=['Food'])


@router.post("/liquid", status_code=201, responses={401: {"description": "Unauthorized"}})
def create_liquid_food_event(request: FoodLiquidRequest, authorized: bool = Depends(authentication)) -> str:
    """
    Receives a 'FoodLiquidRequest' and transforms it into an 'FoodLiquidEvent'
    """
    logging.info(f'Event request: {request}')

    service.launch_event(request)
    return 'Created'

@router_v2.post("/liquid", status_code=201, responses={401: {"description": "Unauthorized"}})
def create_liquid_food_event(request: FoodLiquidRequest, authorized: bool = Depends(authentication)) -> str:
    """
    Receives a 'FoodLiquidRequest' and transforms it into an 'FoodLiquidEvent'
    """
    logging.info(f'Event request: {request}')

    service.launch_event_v2(request)
    return 'Created'
