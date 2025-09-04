from models.time_slot import TimeSlot

from .selector import Selector


class SingleManagerSelector(Selector):
    def __init__(self) -> None:
        super().__init__()

    def select(
        self, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> str | None:
        for volunteer, manager_map in availability_map.items():
            if len(manager_map) == 1:
                return volunteer

        return None
