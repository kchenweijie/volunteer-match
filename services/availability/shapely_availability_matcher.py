from itertools import chain

from shapely.geometry import LineString, MultiLineString
from shapely.geometry.base import BaseGeometry

from models.time_slot import TimeSlot

from .availability_matcher import AvailabilityMatcher


class ShapelyAvailabilityMatcher(AvailabilityMatcher):

    def __init__(self, day_start_time: int, day_end_time: int) -> None:
        super().__init__(day_start_time, day_end_time)

    def get_availability(
        self, manager_busy: list[TimeSlot], volunteer_busy: list[TimeSlot]
    ) -> list[TimeSlot]:
        available: BaseGeometry = LineString(
            [(self._day_start_time, 0), (self._day_end_time, 0)]
        )

        for slot in chain(manager_busy, volunteer_busy):
            busy: LineString = LineString([(slot.start_time, 0), (slot.end_time, 0)])
            available = available.difference(busy)

        if isinstance(available, LineString):
            available_mls: MultiLineString = MultiLineString([available])
        elif isinstance(available, MultiLineString):
            available_mls: MultiLineString = available
        else:
            return []

        return [
            slot
            for subsegment in available_mls.geoms
            for slot in self._to_slots(subsegment)
        ]

    @classmethod
    def _to_slots(cls, linestring: LineString) -> list[TimeSlot]:
        start_coord, *_, end_coord = linestring.coords

        start_time, _ = start_coord
        end_time, _ = end_coord

        return [
            TimeSlot(start_time=sub_start_time, end_time=sub_start_time + 1)
            for sub_start_time in range(int(start_time), int(end_time))
        ]
