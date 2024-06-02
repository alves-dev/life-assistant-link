from builtins import str


class FoodLiquidEvent:
    def __init__(self, person: str, liquid: str, amount: int):
        self.person = person
        self.liquid = liquid.upper()
        self.amount = amount

    def __str__(self):
        return f"FoodLiquidEvent(person={self.person}, liquid={self.liquid}, amount={self.amount})"
