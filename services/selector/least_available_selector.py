from models.time_slot import TimeSlot

from .selector import Selector


class LeastAvailableSelector(Selector):
    def __init__(self) -> None:
        super().__init__()

    def select(
        self, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> str | None:
        return min(
            availability_map.keys(),
            key=lambda volunteer: sum(
                len(slots) for slots in availability_map[volunteer].values()
            ),
            default=None,
        )
