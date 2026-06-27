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
    tasks: List[Task] = field(default_factory=list)

    def add(self) -> None:
        pass

    def edit(self, name: str) -> None:
        pass

    def delete(self) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        return self.tasks


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

    def get_todays_tasks(self) -> List[Task]:
        pass

    def reorder(self) -> None:
        pass

    def summarize(self) -> str:
        pass


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
        self.tasks: List[Task] = []

    def add(self) -> None:
        pass

    def edit(
        self,
        name: str,
        time_available: int,
        preferences: List[str],
    ) -> None:
        pass

    def delete(self) -> None:
        pass

    def generate_schedule(self) -> Schedule:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        schedule = Schedule(schedule_id="", owner_id=self.owner_id, date=datetime.date.today())
        schedule.generate(self, self.pets, all_tasks)
        return schedule
