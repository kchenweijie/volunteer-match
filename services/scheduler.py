import copy

from models.meeting import Meeting
from models.time_slot import TimeSlot

from .availability import AvailabilityMatcher
from .selector import Selector


class Scheduler:

    def __init__(
        self, volunteer_selector: Selector, matcher: AvailabilityMatcher
    ) -> None:
        self._volunteer_selector: Selector = volunteer_selector
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
                mgr for mgr, slots in manager_map.items() if len(slots) == 0
            ]
            for mgr in empty_managers:
                del manager_map[mgr]
        return self._schedule(availability_map, [])

    def _schedule(
        self,
        availability_map: dict[str, dict[str, list[TimeSlot]]],
        meetings: list[Meeting],
    ) -> list[Meeting]:
        # No volunteers remaining
        if len(availability_map) == 0:
            return meetings

        # No manager availability remaining
        if not self._has_manager_availability(availability_map):
            return meetings

        volunteer: str | None = self._volunteer_selector.select(availability_map)

        if volunteer is None:
            return meetings

        longest_subbranch: list[Meeting] = []
        for manager, slots in availability_map[volunteer].items():
            for slot in slots:
                updated_availability_map: dict[str, dict[str, list[TimeSlot]]] = (
                    self._get_updated_availability(
                        availability_map, volunteer, manager, slot
                    )
                )

                subbranch: list[Meeting] = self._schedule(
                    updated_availability_map,
                    meetings + [Meeting(volunteer, manager, slot)],
                )

                # All volunteers have been scheduled, exit early
                if len(subbranch) == len(meetings) + len(availability_map):
                    return subbranch

                if len(subbranch) > len(longest_subbranch):
                    longest_subbranch = subbranch

        return longest_subbranch

    @classmethod
    def _has_manager_availability(
        cls, availability_map: dict[str, dict[str, list[TimeSlot]]]
    ) -> bool:
        return any(len(manager_map) > 0 for manager_map in availability_map.values())

    @classmethod
    def _get_updated_availability(
        cls,
        availability_map: dict[str, dict[str, list[TimeSlot]]],
        volunteer: str,
        manager: str,
        slot: TimeSlot,
    ) -> dict[str, dict[str, list[TimeSlot]]]:
        updated_availability_map: dict[str, dict[str, list[TimeSlot]]] = copy.deepcopy(
            availability_map
        )
        del updated_availability_map[volunteer]

        for manager_map in updated_availability_map.values():
            if manager in manager_map:
                if slot in manager_map[manager]:
                    manager_map[manager].remove(slot)
                if len(manager_map[manager]) == 0:
                    del manager_map[manager]

        return updated_availability_map
