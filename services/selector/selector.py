from abc import ABC, abstractmethod

from models.time_slot import TimeSlot


class Selector(ABC):

    @abstractmethod
    def select(
        self, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> str | None:
        raise NotImplementedError()
