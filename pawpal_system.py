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


@dataclass
class Task:
    task_id: str
    pet_id: str
    task_type: TaskType
    start_time: datetime.time
    duration_minutes: int
    priority: Priority
    explanation: str = ""

    def add(self) -> None:
        pass

    def edit(
        self,
        start_time: datetime.time,
        duration: int,
        priority: Priority,
        task_type: TaskType,
    ) -> None:
        pass

    def delete(self) -> None:
        pass


@dataclass
class Pet:
    pet_id: str
    name: str
    owner_id: str

    def add(self) -> None:
        pass

    def edit(self, name: str) -> None:
        pass

    def delete(self) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Schedule:
    schedule_id: str
    owner_id: str
    date: datetime.date
    tasks: List[Task] = field(default_factory=list)
    generation_explanation: str = ""

    def generate(self, owner: "Owner", pets: List[Pet], tasks: List[Task]) -> None:
        pass

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
        pass
