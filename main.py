from models.meeting import Meeting
from models.time_slot import TimeSlot
from services.availability import AvailabilityMatcher, ShapelyAvailabilityMatcher
from services.scheduler import Scheduler


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
            TimeSlot(start_time=2, end_time=4),
        ],
        "volunteer6": [
            TimeSlot(start_time=8, end_time=9),
            TimeSlot(start_time=12, end_time=13),
        ],
        "volunteer7": [
            TimeSlot(start_time=5, end_time=7),
            TimeSlot(start_time=14, end_time=15),
            TimeSlot(start_time=22, end_time=23),
        ],
        "volunteer8": [
            TimeSlot(start_time=0, end_time=3),
            TimeSlot(start_time=10, end_time=12),
            TimeSlot(start_time=16, end_time=18),
            TimeSlot(start_time=20, end_time=21),
        ],
        "volunteer9": [
            TimeSlot(start_time=7, end_time=8),
            TimeSlot(start_time=9, end_time=11),
            TimeSlot(start_time=13, end_time=14),
            TimeSlot(start_time=15, end_time=17),
            TimeSlot(start_time=18, end_time=20),
        ],
    }

    matcher: AvailabilityMatcher = ShapelyAvailabilityMatcher(
        day_start_time=12, day_end_time=17
    )

    scheduler: Scheduler = Scheduler(matcher=matcher)
    schedule: list[Meeting] = scheduler.schedule(
        manager_busy=manager_busy, volunteer_busy=volunteer_busy
    )

    for volunteer, manager, (start_time, end_time) in schedule:
        print(
            f"Volunteer: {volunteer}, Manager: {manager}, Time: {start_time} --> {end_time}"
        )


if __name__ == "__main__":
    main()
