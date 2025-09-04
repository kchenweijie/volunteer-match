from models.time_slot import TimeSlot

from .selector import Selector


class SequentialSelector(Selector):

    def __init__(self, subselectors: list[Selector]) -> None:
        self._subselectors: list[Selector] = subselectors

    def select(
        self, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> str | None:
        for selector in self._subselectors:
            volunteer: str | None = selector.select(availability_map)
            if volunteer is not None:
                return volunteer

        return None
