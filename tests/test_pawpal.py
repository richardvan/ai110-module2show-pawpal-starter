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


# 3. reorder() — priority then chronological within priority

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
