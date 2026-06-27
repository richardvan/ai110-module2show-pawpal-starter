from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import datetime


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
        self.start_time = start_time
        self.duration_minutes = duration
        self.priority = priority
        self.task_type = task_type
        self.description = description
        if frequency is not None:
            self.frequency = frequency

    def complete(self) -> None:
        self.is_completed = True

    def delete(self, pet: "Pet") -> None:
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
        if self not in owner.pets:
            owner.pets.append(self)

    def edit(self, name: str, species: str = "", breed: str = "", age_years: float = 0.0, notes: str = "") -> None:
        self.name = name
        self.species = species
        self.breed = breed
        self.age_years = age_years
        self.notes = notes

    def delete(self, owner: "Owner") -> None:
        if self in owner.pets:
            owner.pets.remove(self)

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.is_completed]


@dataclass
class Schedule:
    schedule_id: str
    owner_id: str
    date: datetime.date
    tasks: List[Task] = field(default_factory=list)
    generation_explanation: str = ""

    def generate(self, owner: "Owner", pets: List[Pet], tasks: List[Task]) -> None:
        pet_ids = {pet.pet_id for pet in pets}
        self.tasks = [task for task in tasks if task.pet_id in pet_ids]
        self.reorder()

    def get_todays_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.is_completed]

    def get_tasks_by_pet(self, pet_id: str) -> List[Task]:
        return [t for t in self.tasks if t.pet_id == pet_id]

    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        return [t for t in self.tasks if t.task_type == task_type]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        return [t for t in self.tasks if t.priority == priority]

    def reorder(self) -> None:
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        self.tasks.sort(key=lambda t: (priority_order[t.priority], t.start_time))

    def summarize(self) -> str:
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
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_all_pending_tasks(self) -> List[Task]:
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks

    def edit(
        self,
        name: str,
        time_available: int,
        preferences: List[str],
    ) -> None:
        self.name = name
        self.time_available_minutes = time_available
        self.preferences = preferences

    def generate_schedule(self) -> Schedule:
        all_tasks = self.get_all_tasks()
        schedule = Schedule(schedule_id="", owner_id=self.owner_id, date=datetime.date.today())
        schedule.generate(self, self.pets, all_tasks)
        return schedule
