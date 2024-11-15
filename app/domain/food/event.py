from builtins import str
from datetime import datetime
from datetime import datetime as dt

def _formated_date(time: datetime) -> str:
    formatted_date = time.strftime("%Y-%m-%dT%H:%M")
    return formatted_date + '-03:00'


class FoodLiquidEvent:
    """
        Event: https://github.com/alves-dev/life/tree/main/events#alimenta%C3%A7%C3%A3o-routing_key---food-1
    """

    def __init__(self, person_id: str, time: datetime, liquid: str, amount: int):
        self.type = "LIQUID_FOOD"
        self.person_id = person_id
        self.datetime = _formated_date(time)
        self.liquid = liquid.upper()
        self.amount = amount

    def __str__(self):
        return (f"FoodLiquidEvent(type={self.type}, person_id={self.person_id}, datetime={self.datetime},"
                f" liquid={self.liquid}, amount={self.amount})")


class HealthNutriTrackLiquidEvent:

    def __init__(self, person_id: str, time: datetime, liquid: str, amount: int):
        self.type = "HEALTH.NUTRI_TRACK.LIQUID.V1"
        self.person_id = person_id
        self.datetime = time.strftime("%Y-%m-%dT%H:%M")
        self.liquid = liquid
        self.amount = amount
        self.meta_data = {'origin': 'assistant-link', 'created_at': dt.now().strftime("%Y-%m-%dT%H:%M")}

    def __str__(self):
        return (f"HealthNutriTrackLiquidEvent(person_id={self.person_id}, datetime={self.datetime},"
                f" liquid={self.liquid}, amount={self.amount}, meta_data={self.meta_data})")
