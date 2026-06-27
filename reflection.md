# PawPal+ Project Reflection

## 0. Initial Observations and Ideas

**a. Core Actions**

- Identify at least three core actions a user should be able to perform (e.g., add a pet, schedule a walk, see today's task)
	+ Add/edit a owner (owner name)
	+ Add/edit a pet (pet name)
	+ Add/edit a task (start time, duration, priority, task_type)
		* task_type: walk pet, feed food, give meds, provide enrichment, groom)
	+ Generate a daily schedule
		* consider constraints (time available, priority, owner preference)
		* need explanation why this schedule was made this way

**b. Building Blocks**

- Brainstorm the main objects needed for the system. For each object, determine: (What information it needs to hold, i.e. attributes;  What actions it can perform, i.e. methods)
	+ Owner
		* (attributes) name
		* (methods) add, edit, delete
	+ Pet
	   * (attributes) name
	   * (methods) add, edit, delete
	+ Task
	   * (attributes) start_time, duration, priority, task_type
	   * (methods) add, edit, delete
	+ Schedule
	   * (attributes) 
	   * (methods)

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
	+ (My Answer) the Mermaid.js code code provided a class diagram for a pet care app with four entitires - Owner, Pet, Task, Schedule - each with their own attributes and methods. Add/Edit/Delete functionality for Owner, Pet, and Task, class-specific methods for Owner to schedule, the schedule to generate and be sumamrized, to reorder itself, and get todays task.
- What classes did you include, and what responsibilities did you assign to each?
	+ (My Answer) there are four classes: (Owner, Pet, Schedule, Task)
		* an Owner owns a Pet which has any number of Task associated
		* an Owner can generate a Schedule which organizes Task
		* Task are categorized based on five types and ranked by priority. 


**b. Design changes**

- Did your design change during implementation?
	+ (My Answer) Yes, based on feedback from CC
- If yes, describe at least one change and why you made it.
	+ (My Answer) CC notified me of 3 missing relationships and 3 logic issues:
		* Initially I had a redundant function to generate the schedule on both the Owner and Schedule classes, CC recommended I pick a delegation-based approach which keeps the Owner as the public-facing entry point while Schedule does the actual generation. I made this change to keep the logic in the Schedule class, along with changes to Owner to know about the Pets and their associated Task to provide to the Schedule object.
		* I also added more attributes that CC recommended such as having a single source of truth for the Pet's tasks
	

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
	+ (My Answer) first it considers priority then time
- How did you decide which constraints mattered most?
	+ (My Answer) intuitively some tasks just have more priority, so they should be done when scheduled at the same time
	
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
	+ (My Answer) Conflict detection over prevention; the scheduler will add and tasks regardless of overlaps, it will warn after the fact instead of blocking from scheduling the conflicting task
- Why is that tradeoff reasonable for this scenario?
	+ (My Answer) The Owner should be able to see what task they want at what time, and basd on the warnings, can resolve the scheduling conflicts themselves rather than have the Scheduler make decisions for the Owner to resolve

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
