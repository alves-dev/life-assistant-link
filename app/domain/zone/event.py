from enum import Enum
from datetime import datetime


class Action(Enum):
    CAME_IN = 1
    WENT_OUT = 2


class PersonTrackingEvent:
    def __init__(self, action: Action, zone: str, person: str, date: datetime):
        self.action = action
        self.zone = zone
        self.person = person
        self.date = date

    def __str__(self):
        return f"PersonTrackingEvent(action={self.action}, zone={self.zone}, person={self.person}, date={self.date})"
