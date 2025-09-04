from ortools.sat.python import cp_model

from models.time_slot import TimeSlot
from services.availability import AvailabilityMatcher, ShapelyAvailabilityMatcher

_DAY_START: int = 9
_DAY_END: int = 17


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(
        self,
        meetings,
        volunteers: list[str],
        managers: list[str],
        day_start: int,
        day_end: int,
    ):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._meetings = meetings
        self._volunteers: list[str] = volunteers
        self._managers: list[str] = managers
        self._day_start: int = day_start
        self._day_end: int = day_end

    def on_solution_callback(self):
        scheduled_volunteers: set[str] = set()

        for managers in self._managers:
            print(f"Manager: {managers}")

            for start_time in range(self._day_start, self._day_end):
                is_booked: bool = False
                for volunteer in self._volunteers:
                    if self.value(self._meetings[(volunteer, managers, start_time)]):
                        is_booked = True
                        print(f"  {start_time:02d}:00 - {volunteer}")
                        scheduled_volunteers.add(volunteer)

                if not is_booked:
                    print(f"  {start_time:02d}:00 - xxxx")

        unscheduled_volunteers: list[str] = sorted(
            set(self._volunteers) - scheduled_volunteers
        )
        if len(unscheduled_volunteers) > 0:
            print(f"Failed to schedule: {', '.join(unscheduled_volunteers)}")
        else:
            print(f"ALL VOLUNTEERS SCHEDULED!")


def main() -> None:
    manager_busy: dict[str, list[TimeSlot]] = {
        "manager0": [
            TimeSlot(start_time=8, end_time=10),
            TimeSlot(start_time=15, end_time=17),
        ],
        "manager1": [
            TimeSlot(start_time=9, end_time=11),
            TimeSlot(start_time=12, end_time=15),
        ],
        "manager2": [
            TimeSlot(start_time=10, end_time=12),
            TimeSlot(start_time=14, end_time=16),
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
        "volunteer10": [
            TimeSlot(start_time=8, end_time=10),
            TimeSlot(start_time=17, end_time=19),
        ],
        "volunteer11": [
            TimeSlot(start_time=11, end_time=13),
            TimeSlot(start_time=15, end_time=16),
        ],
        "volunteer12": [
            TimeSlot(start_time=10, end_time=12),
            TimeSlot(start_time=18, end_time=20),
        ],
        "volunteer13": [
            TimeSlot(start_time=9, end_time=11),
            TimeSlot(start_time=13, end_time=15),
        ],
        "volunteer14": [
            TimeSlot(start_time=14, end_time=16),
            TimeSlot(start_time=20, end_time=22),
        ],
    }

    model: cp_model.CpModel = cp_model.CpModel()
    meetings: dict[tuple[str, str, int], cp_model.BoolVarT] = {}

    for volunteer in volunteer_busy.keys():
        for manager in manager_busy.keys():
            for start_time in range(_DAY_START, _DAY_END):
                meetings[(volunteer, manager, start_time)] = model.NewBoolVar(
                    f"meeting_{volunteer}_{manager}_{start_time}"
                )

    for manager in manager_busy.keys():
        for start_time in range(_DAY_START, _DAY_END):
            model.add_at_most_one(
                meetings[(volunteer, manager, start_time)]
                for volunteer in volunteer_busy.keys()
            )

    for volunteer in volunteer_busy.keys():
        model.add_at_most_one(
            meetings[(volunteer, manager, start_time)]
            for manager in manager_busy.keys()
            for start_time in range(_DAY_START, _DAY_END)
        )

    availability: dict[str, dict[str, dict[int, int]]] = {
        volunteer: {
            mgr: {slot_start: 0 for slot_start in range(_DAY_START, _DAY_END)}
            for mgr in manager_busy.keys()
        }
        for volunteer in volunteer_busy.keys()
    }
    for volunteer, volunteer_slots in volunteer_busy.items():
        for manager, manager_slots in manager_busy.items():
            matcher: AvailabilityMatcher = ShapelyAvailabilityMatcher(
                _DAY_START, _DAY_END
            )
            available_slots: list[TimeSlot] = matcher.get_availability(
                manager_slots, volunteer_slots
            )
            for slot_start, _ in available_slots:
                availability[volunteer][manager][slot_start] = 1

    model.Maximize(
        sum(
            availability[volunteer][manager][start_time]
            * meetings[(volunteer, manager, start_time)]
            for volunteer in volunteer_busy.keys()
            for manager in manager_busy.keys()
            for start_time in range(_DAY_START, _DAY_END)
        )
    )

    solver: cp_model.CpSolver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    solution_printer: SolutionPrinter = SolutionPrinter(
        meetings,
        list(volunteer_busy.keys()),
        list(manager_busy.keys()),
        _DAY_START,
        _DAY_END,
    )
    res = solver.Solve(model, solution_printer)

    print(f"Solution status: {solver.StatusName(res)}")


if __name__ == "__main__":
    main()
