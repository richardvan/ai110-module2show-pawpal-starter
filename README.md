# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Today's Schedule
Schedule for 2026-06-26 — 6 task(s): 0 completed, 6 pending
  High: 4  Medium: 1  Low: 1
  [○] 07:00:00 | walk_pet | high | Morning walk
  [○] 07:30:00 | walk_pet | high | Morning walk
  [○] 08:00:00 | feed_food | high | Breakfast
  [○] 08:30:00 | feed_food | high | Breakfast
  [○] 16:00:00 | provide_enrichment | medium | Fetch and play session
  [○] 17:00:00 | groom | low | Brush coat

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
========================================== test session starts ===========================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/richardvan/codepath_learning/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 12 items                                                                                       

tests/test_pawpal.py ............                                                                  [100%]

=========================================== 12 passed in 0.01s ===========================================
```

### What the tests cover

**Baseline**
- A task starts as incomplete and becomes complete after calling `complete()`
- Adding a task to a pet increases that pet's task count by 1

**Recurrence logic**
- Completing a daily task returns a new task scheduled for the next day, with the same pet, type, and priority
- Completing a weekly task returns a new task scheduled 7 days later
- Completing a one-time task returns nothing — no follow-up is created

**Conflict detection**
- Two tasks whose time windows overlap are flagged as a conflict
- Two tasks that are back-to-back (one ends exactly when the next begins) are *not* flagged
- Overlapping tasks for different pets are suppressed when `same_pet_only=True`

**Sorting**
- A low-priority task at an earlier time is still ordered after a high-priority task at a later time
- Two tasks at the same priority level stay in chronological order relative to each other

**Schedule integrity**
- Completing a one-time task does not add anything to the schedule's task list
- `generate()` only includes tasks belonging to the pets passed in — tasks for other pets are excluded

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Schedule.reorder()`, `Schedule.sort_by_time()` | `reorder()` sorts by priority then start time; `sort_by_time()` sorts by start time only |
| Filtering | `Owner.filter_tasks()`, `Schedule.get_tasks_by_pet()`, `Schedule.get_tasks_by_type()`, `Schedule.get_tasks_by_priority()` | `filter_tasks()` filters by pet name and/or completion status; the `get_tasks_by_*` methods filter by pet, type, or priority |
| Conflict handling | `Schedule.get_conflicts()`, `Owner.generate_schedule()` | `get_conflicts()` detects overlapping time windows; `generate_schedule()` surfaces them as warning strings |
| Recurring tasks | `Task.complete()`, `Schedule.complete_task()` | `complete()` returns a new Task for the next occurrence (daily +1 day, weekly +7 days); `complete_task()` inserts it into the schedule automatically |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
