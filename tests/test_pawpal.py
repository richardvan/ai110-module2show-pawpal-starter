import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Schedule, Owner, TaskType, Priority, Frequency
import datetime


def make_pet():
    return Pet(pet_id="p1", owner_id="o1", name="Rex", species="Dog")


def make_task(pet_id="p1"):
    return Task(
        task_id="t1",
        pet_id=pet_id,
        task_type=TaskType.WALK_PET,
        description="Morning walk",
        start_time=datetime.time(8, 0),
        duration_minutes=30,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY,
    )


def test_complete_changes_task_status():
    task = make_task()
    assert task.is_completed is False
    task.complete()
    assert task.is_completed is True


def test_adding_task_increases_pet_task_count():
    pet = make_pet()
    assert len(pet.get_tasks()) == 0
    task = make_task(pet_id=pet.pet_id)
    task.add(pet)
    assert len(pet.get_tasks()) == 1


def make_schedule(tasks=None):
    return Schedule(
        schedule_id="s1",
        owner_id="o1",
        date=datetime.date(2026, 1, 1),
        tasks=tasks or [],
    )


# 1. Recurring task chaining

def test_complete_daily_returns_next_day_task():
    task = make_task()
    on_date = datetime.date(2026, 1, 1)
    next_task = task.complete(on_date=on_date)
    assert next_task is not None
    assert next_task.is_completed is False
    assert "2026-01-02" in next_task.task_id
    assert next_task.pet_id == task.pet_id
    assert next_task.task_type == task.task_type
    assert next_task.priority == task.priority


def test_complete_weekly_returns_seven_days_later():
    task = Task(
        task_id="t2", pet_id="p1", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(8, 0), duration_minutes=15,
        priority=Priority.MEDIUM, frequency=Frequency.WEEKLY,
    )
    on_date = datetime.date(2026, 1, 1)
    next_task = task.complete(on_date=on_date)
    assert next_task is not None
    assert "2026-01-08" in next_task.task_id


def test_complete_once_returns_none():
    task = Task(
        task_id="t3", pet_id="p1", task_type=TaskType.GROOM,
        start_time=datetime.time(10, 0), duration_minutes=60,
        priority=Priority.LOW, frequency=Frequency.ONCE,
    )
    assert task.complete() is None


# 2. Conflict detection

def test_overlapping_tasks_detected_as_conflict():
    t1 = make_task()  # 08:00–08:30
    t2 = Task(
        task_id="t2", pet_id="p1", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(8, 15), duration_minutes=30,
        priority=Priority.MEDIUM,
    )
    schedule = make_schedule([t1, t2])
    assert len(schedule.get_conflicts()) == 1


def test_back_to_back_tasks_not_a_conflict():
    t1 = make_task()  # 08:00–08:30
    t2 = Task(
        task_id="t2", pet_id="p1", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(8, 30), duration_minutes=15,
        priority=Priority.MEDIUM,
    )
    schedule = make_schedule([t1, t2])
    assert len(schedule.get_conflicts()) == 0


def test_same_pet_only_suppresses_cross_pet_conflicts():
    t1 = make_task(pet_id="p1")  # 08:00–08:30
    t2 = Task(
        task_id="t2", pet_id="p2", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(8, 0), duration_minutes=30,
        priority=Priority.MEDIUM,
    )
    schedule = make_schedule([t1, t2])
    assert len(schedule.get_conflicts(same_pet_only=True)) == 0
    assert len(schedule.get_conflicts(same_pet_only=False)) == 1


# 3. Find next available slot

def test_find_slot_returns_day_start_when_pet_has_no_tasks():
    pet = make_pet()

    assert pet.find_next_available_slot(30) == datetime.time(7, 0)


def test_find_slot_skips_past_conflicting_task():
    pet = make_pet()
    pet.tasks = [
        Task(
            task_id="t_block",
            pet_id=pet.pet_id,
            task_type=TaskType.WALK_PET,
            start_time=datetime.time(8, 0),
            duration_minutes=30,
            priority=Priority.HIGH,
        )
    ]

    assert pet.find_next_available_slot(30, day_start=datetime.time(8, 0)) == datetime.time(8, 30)


def test_find_slot_respects_back_to_back_as_free():
    pet = make_pet()
    pet.tasks = [
        Task(
            task_id="t_block",
            pet_id=pet.pet_id,
            task_type=TaskType.WALK_PET,
            start_time=datetime.time(8, 0),
            duration_minutes=30,
            priority=Priority.HIGH,
        )
    ]

    assert pet.find_next_available_slot(15, day_start=datetime.time(8, 30)) == datetime.time(8, 30)


def test_find_slot_returns_none_when_day_is_fully_booked():
    pet = make_pet()
    pet.tasks = [
        Task(
            task_id="t_block",
            pet_id=pet.pet_id,
            task_type=TaskType.WALK_PET,
            start_time=datetime.time(8, 0),
            duration_minutes=60,
            priority=Priority.HIGH,
        )
    ]

    assert pet.find_next_available_slot(30, day_start=datetime.time(8, 0), day_end=datetime.time(9, 0)) is None


def test_find_slot_returns_none_when_duration_exceeds_window():
    pet = make_pet()

    assert pet.find_next_available_slot(90, day_start=datetime.time(8, 0), day_end=datetime.time(9, 0)) is None


def test_find_slot_ignores_other_pets_tasks():
    p1 = make_pet()
    p2 = Pet(pet_id="p2", owner_id="o1", name="Milo", species="Cat")
    p1.tasks = [
        Task(
            task_id="t_block",
            pet_id=p1.pet_id,
            task_type=TaskType.WALK_PET,
            start_time=datetime.time(8, 0),
            duration_minutes=60,
            priority=Priority.HIGH,
        )
    ]

    assert p2.find_next_available_slot(30, day_start=datetime.time(8, 0)) == datetime.time(8, 0)


def test_find_slot_custom_step_size():
    pet = make_pet()
    pet.tasks = [
        Task(
            task_id="t_block",
            pet_id=pet.pet_id,
            task_type=TaskType.WALK_PET,
            start_time=datetime.time(8, 0),
            duration_minutes=20,
            priority=Priority.HIGH,
        )
    ]

    assert pet.find_next_available_slot(20, day_start=datetime.time(8, 0), step_minutes=10) == datetime.time(8, 20)


# 4. reorder() — priority then chronological within priority

def test_reorder_puts_high_before_low_regardless_of_time():
    low_early = Task(
        task_id="t_low", pet_id="p1", task_type=TaskType.GROOM,
        start_time=datetime.time(7, 0), duration_minutes=30,
        priority=Priority.LOW,
    )
    high_late = make_task()  # HIGH at 08:00
    schedule = make_schedule([low_early, high_late])
    schedule.reorder()
    assert schedule.tasks[0].priority == Priority.HIGH


def test_reorder_preserves_time_order_within_same_priority():
    t1 = make_task()  # HIGH 08:00
    t2 = Task(
        task_id="t2", pet_id="p1", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(9, 0), duration_minutes=15,
        priority=Priority.HIGH,
    )
    schedule = make_schedule([t2, t1])
    schedule.reorder()
    assert schedule.tasks[0].start_time == datetime.time(8, 0)
    assert schedule.tasks[1].start_time == datetime.time(9, 0)


# 4. complete_task on non-recurring does not grow task list

def test_complete_task_once_does_not_append():
    task = Task(
        task_id="t_once", pet_id="p1", task_type=TaskType.GROOM,
        start_time=datetime.time(10, 0), duration_minutes=60,
        priority=Priority.LOW, frequency=Frequency.ONCE,
    )
    schedule = make_schedule([task])
    result = schedule.complete_task(task)
    assert result is None
    assert len(schedule.tasks) == 1


# 5. generate() filters to only matching pets

def test_generate_excludes_tasks_for_other_pets():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()
    owner.add_pet(pet)

    task_mine = make_task(pet_id="p1")
    task_other = Task(
        task_id="t_other", pet_id="p99", task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(9, 0), duration_minutes=15,
        priority=Priority.MEDIUM,
    )
    schedule = make_schedule()
    schedule.generate(owner, [pet], [task_mine, task_other])
    assert all(t.pet_id == "p1" for t in schedule.tasks)
    assert len(schedule.tasks) == 1


# 6. Owner helpers and filters

def test_owner_filter_tasks_is_case_insensitive_and_respects_completion():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()
    other_pet = Pet(pet_id="p2", owner_id="o1", name="Milo", species="Cat")
    owner.add_pet(pet)
    owner.add_pet(other_pet)

    pending_task = make_task(pet_id=pet.pet_id)
    completed_task = Task(
        task_id="t_done",
        pet_id=pet.pet_id,
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(12, 0),
        duration_minutes=10,
        priority=Priority.LOW,
    )
    completed_task.complete()
    other_task = Task(
        task_id="t_other",
        pet_id=other_pet.pet_id,
        task_type=TaskType.GROOM,
        start_time=datetime.time(13, 0),
        duration_minutes=20,
        priority=Priority.MEDIUM,
    )
    pet.tasks = [pending_task, completed_task]
    other_pet.tasks = [other_task]

    assert owner.filter_tasks(pet_name="rex") == [pending_task, completed_task]
    assert owner.filter_tasks(is_completed=False) == [pending_task, other_task]
    assert owner.filter_tasks(is_completed=True) == [completed_task]
    assert owner.filter_tasks(is_completed=False, pet_name="REX") == [pending_task]


def test_owner_pet_lookup_and_removal_work():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()

    assert owner.get_pet("p1") is None
    owner.add_pet(pet)
    assert owner.get_pet("p1") is pet

    owner.remove_pet(pet)
    assert owner.get_pet("p1") is None


def test_pending_task_helpers_return_only_incomplete_tasks():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()
    owner.add_pet(pet)

    pending_task = make_task(pet_id=pet.pet_id)
    completed_task = Task(
        task_id="t_done",
        pet_id=pet.pet_id,
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(12, 0),
        duration_minutes=10,
        priority=Priority.LOW,
    )
    completed_task.complete()
    pet.tasks = [pending_task, completed_task]

    assert pet.get_pending_tasks() == [pending_task]
    assert owner.get_all_pending_tasks() == [pending_task]


def test_schedule_lookup_methods_filter_by_pet_type_and_priority():
    task_high = make_task(pet_id="p1")
    task_medium = Task(
        task_id="t2",
        pet_id="p2",
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(9, 0),
        duration_minutes=15,
        priority=Priority.MEDIUM,
    )
    task_low = Task(
        task_id="t3",
        pet_id="p1",
        task_type=TaskType.GROOM,
        start_time=datetime.time(10, 0),
        duration_minutes=20,
        priority=Priority.LOW,
    )
    schedule = make_schedule([task_high, task_medium, task_low])

    assert schedule.get_tasks_by_pet("p1") == [task_high, task_low]
    assert schedule.get_tasks_by_type(TaskType.FEED_FOOD) == [task_medium]
    assert schedule.get_tasks_by_priority(Priority.HIGH) == [task_high]


# 7. Recurrence and reporting

def test_complete_task_recurring_appends_next_task():
    task = make_task()
    schedule = make_schedule([task])

    result = schedule.complete_task(task)

    assert result is not None
    assert task.is_completed is True
    assert len(schedule.tasks) == 2
    assert result in schedule.tasks
    assert "2026-01-02" in result.task_id


def test_summarize_reports_counts_and_statuses():
    completed_task = make_task()
    completed_task.complete()
    pending_task = Task(
        task_id="t2",
        pet_id="p1",
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(9, 0),
        duration_minutes=15,
        priority=Priority.LOW,
    )
    schedule = make_schedule([completed_task, pending_task])

    summary = schedule.summarize()

    assert "2 task(s): 1 completed, 1 pending" in summary
    assert "High: 1  Medium: 0  Low: 1" in summary
    assert "[✓]" in summary
    assert "[○]" in summary


def test_generate_schedule_returns_conflict_warnings():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()
    owner.add_pet(pet)

    first = make_task(pet_id=pet.pet_id)
    second = Task(
        task_id="t2",
        pet_id=pet.pet_id,
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(8, 15),
        duration_minutes=20,
        priority=Priority.MEDIUM,
    )
    pet.tasks = [first, second]

    schedule, warnings = owner.generate_schedule()

    assert len(schedule.tasks) == 2
    assert len(warnings) == 1
    assert "overlaps" in warnings[0]


def test_generate_schedule_returns_no_warnings_when_tasks_do_not_overlap():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)
    pet = make_pet()
    owner.add_pet(pet)

    first = make_task(pet_id=pet.pet_id)
    second = Task(
        task_id="t2",
        pet_id=pet.pet_id,
        task_type=TaskType.FEED_FOOD,
        start_time=datetime.time(9, 0),
        duration_minutes=20,
        priority=Priority.MEDIUM,
    )
    pet.tasks = [first, second]

    schedule, warnings = owner.generate_schedule()

    assert len(schedule.tasks) == 2
    assert warnings == []


def test_generate_schedule_handles_empty_owner():
    owner = Owner(owner_id="o1", name="Alice", time_available_minutes=120)

    schedule, warnings = owner.generate_schedule()

    assert schedule.tasks == []
    assert warnings == []


# 8. Edit methods and sorting edge cases

def test_task_edit_updates_all_requested_fields():
    task = make_task()

    task.edit(
        start_time=datetime.time(11, 30),
        duration=45,
        priority=Priority.LOW,
        task_type=TaskType.GROOM,
        description="Afternoon groom",
        frequency=Frequency.WEEKLY,
    )

    assert task.start_time == datetime.time(11, 30)
    assert task.duration_minutes == 45
    assert task.priority == Priority.LOW
    assert task.task_type == TaskType.GROOM
    assert task.description == "Afternoon groom"
    assert task.frequency == Frequency.WEEKLY


def test_task_edit_keeps_frequency_when_not_provided():
    task = make_task()

    task.edit(
        start_time=datetime.time(9, 15),
        duration=20,
        priority=Priority.MEDIUM,
        task_type=TaskType.FEED_FOOD,
        description="Changed",
    )

    assert task.frequency == Frequency.DAILY


def test_pet_edit_updates_profile_fields():
    pet = make_pet()

    pet.edit(
        name="Ziggy",
        species="Cat",
        breed="Tabby",
        age_years=4.5,
        notes="Curious and calm",
    )

    assert pet.name == "Ziggy"
    assert pet.species == "Cat"
    assert pet.breed == "Tabby"
    assert pet.age_years == 4.5
    assert pet.notes == "Curious and calm"


def test_sort_by_time_orders_tasks_chronologically_only():
    late_high = Task(
        task_id="t1",
        pet_id="p1",
        task_type=TaskType.WALK_PET,
        start_time=datetime.time(18, 0),
        duration_minutes=30,
        priority=Priority.HIGH,
    )
    early_low = Task(
        task_id="t2",
        pet_id="p1",
        task_type=TaskType.GROOM,
        start_time=datetime.time(7, 0),
        duration_minutes=20,
        priority=Priority.LOW,
    )
    schedule = make_schedule([late_high, early_low])

    schedule.sort_by_time()

    assert schedule.tasks == [early_low, late_high]


def test_complete_monthly_returns_none_and_marks_task_complete():
    task = Task(
        task_id="t_monthly",
        pet_id="p1",
        task_type=TaskType.GROOM,
        start_time=datetime.time(10, 0),
        duration_minutes=60,
        priority=Priority.LOW,
        frequency=Frequency.MONTHLY,
    )

    result = task.complete(on_date=datetime.date(2026, 1, 1))

    assert result is None
    assert task.is_completed is True
