from abc import ABC, abstractmethod

from models.time_slot import TimeSlot


class AvailabilityMatcher(ABC):

    def __init__(self, day_start_time: int, day_end_time: int) -> None:
        self._day_start_time: int = day_start_time
        self._day_end_time: int = day_end_time

    @abstractmethod
    def get_availability(
        self, manager_busy: list[TimeSlot], volunteer_busy: list[TimeSlot]
    ) -> list[TimeSlot]:
        raise NotImplementedError()
