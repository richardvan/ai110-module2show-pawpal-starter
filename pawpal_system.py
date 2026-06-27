from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime
import itertools


class TaskType(Enum):
    WALK_PET = "walk_pet"
    FEED_FOOD = "feed_food"
    GIVE_MEDS = "give_meds"
    PROVIDE_ENRICHMENT = "provide_enrichment"
    GROOM = "groom"


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Frequency(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    task_id: str
    pet_id: str
    task_type: TaskType
    start_time: datetime.time
    duration_minutes: int
    priority: Priority
    description: str = ""
    frequency: Frequency = Frequency.DAILY
    is_completed: bool = False
    explanation: str = ""

    def add(self, pet: "Pet") -> None:
        """Add this task to a pet's task list if not already present."""
        if self not in pet.tasks:
            pet.tasks.append(self)

    def edit(
        self,
        start_time: datetime.time,
        duration: int,
        priority: Priority,
        task_type: TaskType,
        description: str = "",
        frequency: Optional["Frequency"] = None,
    ) -> None:
        """Update the task's scheduling details and type."""
        self.start_time = start_time
        self.duration_minutes = duration
        self.priority = priority
        self.task_type = task_type
        self.description = description
        if frequency is not None:
            self.frequency = frequency

    def complete(self, on_date: Optional[datetime.date] = None) -> Optional["Task"]:
        """Mark this task completed and return a new Task for the next occurrence if recurring.

        Returns a new Task for DAILY (next day) or WEEKLY (next week) frequencies,
        or None for ONCE/MONTHLY tasks.
        """
        self.is_completed = True
        if self.frequency not in (Frequency.DAILY, Frequency.WEEKLY):
            return None
        base = on_date or datetime.date.today()
        delta = datetime.timedelta(days=1 if self.frequency == Frequency.DAILY else 7)
        next_date = base + delta
        return Task(
            task_id=f"{self.task_id}_{next_date.isoformat()}",
            pet_id=self.pet_id,
            task_type=self.task_type,
            start_time=self.start_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            description=self.description,
            frequency=self.frequency,
        )

    def delete(self, pet: "Pet") -> None:
        """Remove this task from a pet's task list."""
        if self in pet.tasks:
            pet.tasks.remove(self)


@dataclass
class Pet:
    pet_id: str
    name: str
    owner_id: str
    species: str = ""
    breed: str = ""
    age_years: float = 0.0
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add(self, owner: "Owner") -> None:
        """Register this pet with an owner if not already registered."""
        if self not in owner.pets:
            owner.pets.append(self)

    def edit(self, name: str, species: str = "", breed: str = "", age_years: float = 0.0, notes: str = "") -> None:
        """Update the pet's profile information."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age_years = age_years
        self.notes = notes

    def delete(self, owner: "Owner") -> None:
        """Remove this pet from an owner's pet list."""
        if self in owner.pets:
            owner.pets.remove(self)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.is_completed]


@dataclass
class Schedule:
    schedule_id: str
    owner_id: str
    date: datetime.date
    tasks: List[Task] = field(default_factory=list)
    generation_explanation: str = ""

    def generate(self, owner: "Owner", pets: List[Pet], tasks: List[Task]) -> None:
        """Populate the schedule with tasks belonging to the given pets, then sort them."""
        pet_ids = {pet.pet_id for pet in pets}
        self.tasks = [task for task in tasks if task.pet_id in pet_ids]
        self.reorder()

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if recurring, add its next occurrence to the schedule.

        Returns the newly created follow-up Task, or None for non-recurring tasks.
        """
        next_task = task.complete(on_date=self.date)
        if next_task is not None:
            self.tasks.append(next_task)
            self.reorder()
        return next_task

    def get_todays_tasks(self) -> List[Task]:
        """Return all incomplete tasks for today."""
        return [t for t in self.tasks if not t.is_completed]

    def get_tasks_by_pet(self, pet_id: str) -> List[Task]:
        """Return all tasks in the schedule for a specific pet."""
        return [t for t in self.tasks if t.pet_id == pet_id]

    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        """Return all tasks in the schedule matching a given task type."""
        return [t for t in self.tasks if t.task_type == task_type]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Return all tasks in the schedule with the specified priority level."""
        return [t for t in self.tasks if t.priority == priority]

    def get_conflicts(self, same_pet_only: bool = False) -> List[tuple]:
        """Return pairs of tasks whose time windows overlap.

        Each result is a (task_a, task_b) tuple. Pass same_pet_only=True to
        restrict to conflicts between tasks for the same pet.
        """
        anchor = datetime.date.today()
        conflicts = []
        for i, a in enumerate(self.tasks):
            a_start = datetime.datetime.combine(anchor, a.start_time)
            a_end = a_start + datetime.timedelta(minutes=a.duration_minutes)
            for b in self.tasks[i + 1:]:
                if same_pet_only and a.pet_id != b.pet_id:
                    continue
                b_start = datetime.datetime.combine(anchor, b.start_time)
                b_end = b_start + datetime.timedelta(minutes=b.duration_minutes)
                if a_start < b_end and b_start < a_end:
                    conflicts.append((a, b))
        return conflicts

    def sort_by_time(self) -> None:
        """Sort tasks by start time in chronological order."""
        self.tasks = sorted(self.tasks, key=lambda t: t.start_time)

    def reorder(self) -> None:
        """Sort tasks by priority then start time."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        self.tasks.sort(key=lambda t: (priority_order[t.priority], t.start_time))

    def summarize(self) -> str:
        """Return a formatted string summary of the schedule's tasks and completion status."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.is_completed)
        pending = total - completed
        by_priority = {p: 0 for p in Priority}
        for t in self.tasks:
            by_priority[t.priority] += 1
        lines = [
            f"Schedule for {self.date} — {total} task(s): {completed} completed, {pending} pending",
            f"  High: {by_priority[Priority.HIGH]}  Medium: {by_priority[Priority.MEDIUM]}  Low: {by_priority[Priority.LOW]}",
        ]
        for t in self.tasks:
            status = "✓" if t.is_completed else "○"
            lines.append(f"  [{status}] {t.start_time} | {t.task_type.value} | {t.priority.value} | {t.description}")
        return "\n".join(lines)


class Owner:
    def __init__(
        self,
        owner_id: str,
        name: str,
        time_available_minutes: int,
        preferences: Optional[List[str]] = None,
    ):
        self.owner_id = owner_id
        self.name = name
        self.time_available_minutes = time_available_minutes
        self.preferences: List[str] = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Look up and return a pet by its ID, or None if not found."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet the owner has."""
        return list(itertools.chain.from_iterable(pet.tasks for pet in self.pets))

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across every pet the owner has."""
        return [t for t in self.get_all_tasks() if not t.is_completed]

    def edit(
        self,
        name: str,
        time_available: int,
        preferences: List[str],
    ) -> None:
        """Update the owner's name, availability, and care preferences."""
        self.name = name
        self.time_available_minutes = time_available
        self.preferences = preferences

    def filter_tasks(
        self,
        is_completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name (case-insensitive)."""
        results = []
        for pet in self.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if is_completed is not None and task.is_completed != is_completed:
                    continue
                results.append(task)
        return results

    def generate_schedule(self) -> tuple:
        """Build a sorted Schedule and return (schedule, warnings).

        warnings is a list of human-readable strings, one per detected conflict.
        It is empty when no conflicts exist.
        """
        all_tasks = self.get_all_tasks()
        schedule = Schedule(schedule_id="", owner_id=self.owner_id, date=datetime.date.today())
        schedule.generate(self, self.pets, all_tasks)

        pet_name_by_id = {pet.pet_id: pet.name for pet in self.pets}
        warnings = []
        for a, b in schedule.get_conflicts():
            a_pet = pet_name_by_id.get(a.pet_id, a.pet_id)
            b_pet = pet_name_by_id.get(b.pet_id, b.pet_id)
            warnings.append(
                f"WARNING: '{a.description}' ({a_pet}, {a.start_time}) "
                f"overlaps '{b.description}' ({b_pet}, {b.start_time})"
            )
        return schedule, warnings
