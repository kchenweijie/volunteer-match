from models.meeting import Meeting
from models.time_slot import TimeSlot
from services.availability import AvailabilityMatcher, ShapelyAvailabilityMatcher


def main() -> None:
    manager_busy: dict[str, list[TimeSlot]] = {
        "manager0": [
            TimeSlot(start_time=8, end_time=10),
            TimeSlot(start_time=15, end_time=17),
        ],
        "manager1": [
            TimeSlot(start_time=9, end_time=11),
            TimeSlot(start_time=12, end_time=14),
        ],
    }

    volunteer_busy: dict[str, list[TimeSlot]] = {
        "volunteer0": [
            TimeSlot(start_time=15, end_time=16),
            TimeSlot(start_time=19, end_time=22),
        ],
        "volunteer1": [
            TimeSlot(start_time=14, end_time=18),
            TimeSlot(start_time=20, end_time=21),
        ],
        "volunteer2": [
            TimeSlot(start_time=9, end_time=10),
            TimeSlot(start_time=12, end_time=13),
            TimeSlot(start_time=13, end_time=14),
            TimeSlot(start_time=18, end_time=19),
        ],
        "volunteer3": [
            TimeSlot(start_time=9, end_time=12),
            TimeSlot(start_time=13, end_time=18),
        ],
        "volunteer4": [
            TimeSlot(start_time=0, end_time=2),
            TimeSlot(start_time=15, end_time=17),
        ],
        "volunteer5": [
            TimeSlot(start_time=3, end_time=5),
        ],
        "volunteer6": [
            TimeSlot(start_time=6, end_time=8),
            TimeSlot(start_time=15, end_time=16),
        ],
        "volunteer7": [
            TimeSlot(start_time=10, end_time=12),
            TimeSlot(start_time=20, end_time=23),
        ],
        "volunteer8": [
            TimeSlot(start_time=0, end_time=1),
            TimeSlot(start_time=13, end_time=15),
        ],
        "volunteer9": [
            TimeSlot(start_time=17, end_time=19),
            TimeSlot(start_time=21, end_time=23),
        ],
    }

    matcher: AvailabilityMatcher = ShapelyAvailabilityMatcher(
        day_start_time=8, day_end_time=17
    )
    availability_map: dict[str, dict[str, list[TimeSlot]]] = {
        volunteer: {
            manager: matcher.get_availability(manager_slots, volunteer_slots)
            for manager, manager_slots in manager_busy.items()
        }
        for volunteer, volunteer_slots in volunteer_busy.items()
    }


if __name__ == "__main__":
    main()
