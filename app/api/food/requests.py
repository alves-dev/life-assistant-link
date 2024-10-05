from pydantic import BaseModel, Field
from datetime import datetime as dt


class FoodLiquidRequest(BaseModel):
    person: str
    liquid: str
    amount: int
    datetime: dt = Field(default_factory=dt.now)
