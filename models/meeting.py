from typing import NamedTuple

from .time_slot import TimeSlot


class Meeting(NamedTuple):
    volunteer: str
    manager: str
    time_slot: TimeSlot
