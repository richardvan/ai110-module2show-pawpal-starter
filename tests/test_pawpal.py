import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, TaskType, Priority, Frequency
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
