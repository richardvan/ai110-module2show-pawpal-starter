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
	+ (My Answer) Claude Code, either Sonnet or Haiku models, were used extensively throughout this project.  Although, I did not use AI during the initial observations and brainstorming as I read through the problem statement on the project website.  I used AI from my generation of the UML draft diagram with mermaid.live code, through implementation of classes, methods, bug fixes, and further enhancements.
- What kinds of prompts or questions were most helpful?
	+ (My Answer) Prompts that are specific and small in scope, from the last project I learned to open a new Claude Code window when fixing different bugs or implementing new features, and I practiced highlighting the code lines of interest to ask Claude Code to help me with those sections, describing what I expected to see happen.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

	+ (My Answer) When certain UI buttons didn't have confirmation buttons, had to work through that behavior from the User-side of what behavior is expected.  The information would just be silented updated, but the User doesn't know that so I worked with CC to close the expanded section and also provide a message.

- How did you evaluate or verify what the AI suggested?

	+ (My Answer) I would completely stop the app (CTRL + C) and restart it via command line (`streamlit run app.py`) in order to make sure any changes were reflected.  Previously, I thought just refreshing the page would work, but it didn't for this particular project. Then I tested added a pet and task, modifying/deleting the task to see what UI behavior was happening upon each click.  I would ask myself if this was intuitive for someone using the app for the same time or if it seemed buggy.  I would work with the AI until the former situiation was reached.  

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
	+ (My Answer) the association between task, pets, and owner was important and I followed the UML diagram to keep me focused on the expected behavior.  The behavior of the scheduler was tested by scheduling recurrent task and making sure they actually do recur, also conflicts were detected and flagged.  Editing task, pets, and owner also required testing by trying out the UI itself to get a feel for the user experience.
- Why were these tests important?
	+ (My Answer) these test are important for the app to work as expected by the user.  Users probably have had experience with other scheduling apps and functions before, so it's important to replicate the expected behavior a user is used to with scheduling anything.  Test the app extensively helps prevent the user from getting to a wierd state of the app where it feels glitchy or becomes unusable.

**b. Confidence**

- How confident are you that your scheduler works correctly?
	+ (My Answer) I believe my scheduler works as intended for how I understood the problem statement, as it generates the schedule when you click "Generate schedule" button.  I tried many different scenarios for conflicts and recurring task, but there could be certain cases such as adding thousands of task that might clutter the schedule or not display everything.
- What edge cases would you test next if you had more time?
	+ (My Answer) there are some minor things such as inputting numbers into the "Species" field, this doesn't necessarily break the app, but perhaps it could warn the user.  You can also add a pet of the exact same name, which could be what the user wants or they "Add pet" button was clicked twice so they could ask the User for confirmation they want this.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
	+ (My Answer) using AI to tackle small problems, at first the project seemed overwhelming, but I put 30 mins to an hour of time into this project over multiple days to work towards building out the app.  It was sort of fun in a way to work with the AI to get things done.  I typically use Haiku to keep the token usage low, but I do notice that it makes mistake sometimes, but if I point them out then Haiku will fix its mistake.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
	+ (My Answer) certain UI elements like putting the "Start hour (0-23)" and "Start minute" could be improved to actually be UI time controls that you scroll through a digital for to specify these options.	

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
	+ (My Answer) it is generally a good idea to be specific about what you want the AI to do for you and you can do this by highlighting the code for it to change and telling the AI how you expect the app to function.  The AI is good as figuring out things for you and I like that sometimes it provides different options for you to choose from.  The design phase of the system was previously difficult for me in the past, but working through this project and the related tinker lab has helped me gain more experience to start with a UML design and to consider it throughout the development of an app.
