from models.time_slot import TimeSlot

from .selector import Selector


class SingleSlotSelector(Selector):
    def __init__(self) -> None:
        super().__init__()

    def select(
        self, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> str | None:
        for volunteer, manager_map in availability_map.items():
            if sum(len(slots) for slots in manager_map.values()) == 0:
                return volunteer

        return None
