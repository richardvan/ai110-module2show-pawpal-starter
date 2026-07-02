# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**


(Claude Code Haiku) I asked Claude Code to explore the codebase and design a "find next available slot" algorithmic feature for the PawPal scheduling app. The feature would find the first non-conflicting time slot for a pet's tasks and surface it in the task scheduler UI.

(Codex 5.4-Mini Light) I asked the agent to implement the planned "find next available slot" feature by refactoring overlap logic, adding a pet-level slot search method, wiring it into the Streamlit task scheduler, and adding tests.


**What did the agent do?**

(Claude Code Haiku) An Explore agent read through `pawpal_system.py` and `app.py` to understand the Task/Schedule/Pet/Owner data model, conflict detection logic, and the current Streamlit UI structure. Then a Plan agent designed a detailed implementation approach covering: (1) extracting a shared `_intervals_overlap()` helper function to avoid code duplication, (2) adding a `Pet.find_next_available_slot()` method that walks a configurable day window (7am–9pm by default, 15-min steps) to find the first free slot, (3) UI integration in the "Schedule a Task" form using a suggestion button and session_state prefilling, and (4) comprehensive test cases covering all edge cases.


(Codex 5.4-Mini Light) It read the plan and the existing code first, then updated `pawpal_system.py`, `app.py`, and `tests/test_pawpal.py`, and finally ran `pytest -q` to verify the changes.


**What did you have to verify or fix manually?**

(My Answer) I checked the behavior of the new "Find next available slot" button and it led to a Streamlit Error message, which I provided back to Codex and ask for a fix.  After this I reviewed the final UI wording and layout choices, and I confirmed the implementation of the new feature.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
