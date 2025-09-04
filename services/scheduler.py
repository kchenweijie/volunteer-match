import copy

from models.meeting import Meeting
from models.time_slot import TimeSlot

from .availability import AvailabilityMatcher
from .selector import (
    LeastAvailableSelector,
    Selector,
    SingleManagerSelector,
    SingleSlotSelector,
)


class Scheduler:

    _SELECTORS: list[Selector] = [
        SingleSlotSelector(),
        SingleManagerSelector(),
        LeastAvailableSelector(),
    ]

    def __init__(self, matcher: AvailabilityMatcher) -> None:
        self._matcher: AvailabilityMatcher = matcher

    def schedule(
        self,
        manager_busy: dict[str, list[TimeSlot]],
        volunteer_busy: dict[str, list[TimeSlot]],
    ) -> list[Meeting]:
        availability_map: dict[str, dict[str, list[TimeSlot]]] = {
            volunteer: {
                manager: self._matcher.get_availability(manager_slots, volunteer_slots)
                for manager, manager_slots in manager_busy.items()
            }
            for volunteer, volunteer_slots in volunteer_busy.items()
        }
        for manager_map in availability_map.values():
            empty_managers: list[str] = [
                m for m, slots in manager_map.items() if len(slots) == 0
            ]
            for m in empty_managers:
                del manager_map[m]
        return self._schedule(availability_map, [])

    def _schedule(
        self,
        availability_map: dict[str, dict[str, list[TimeSlot]]],
        meetings: list[Meeting],
    ) -> list[Meeting]:
        if len(availability_map) == 0:
            return meetings

        if (
            sum(
                len(slots)
                for manager_map in availability_map.values()
                for slots in manager_map.values()
            )
            == 0
        ):
            return meetings

        volunteer: str | None = self._select_volunteer(availability_map)

        if volunteer is None:
            return meetings

        longest_subbranch: list[Meeting] = []
        for manager, slots in availability_map[volunteer].items():
            for slot in slots:
                updated_availability_map: dict[str, dict[str, list[TimeSlot]]] = (
                    copy.deepcopy(availability_map)
                )
                del updated_availability_map[volunteer]

                for manager_map in updated_availability_map.values():
                    if manager in manager_map:
                        manager_map[manager] = [
                            s
                            for s in manager_map[manager]
                            if not (
                                s.start_time < slot.end_time
                                and slot.start_time < s.end_time
                            )
                        ]
                        if len(manager_map[manager]) == 0:
                            del manager_map[manager]

                subbranch: list[Meeting] = self._schedule(
                    updated_availability_map,
                    meetings + [Meeting(volunteer, manager, slot)],
                )

                if len(subbranch) == len(meetings) + len(availability_map):
                    return subbranch

                if len(subbranch) > len(longest_subbranch):
                    longest_subbranch = subbranch

        return longest_subbranch

    def _select_volunteer(
        self,
        availability_map: dict[str, dict[str, list[TimeSlot]]],
    ) -> str | None:
        for selector in self._SELECTORS:
            volunteer: str | None = selector.select(availability_map)
            if volunteer is not None:
                return volunteer

        return None
