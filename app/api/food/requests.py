from pydantic import BaseModel
from datetime import datetime as dt


class FoodLiquidRequest(BaseModel):
    person: str
    liquid: str
    amount: int
    datetime: dt = dt.now()
