import streamlit as st
import datetime
from pawpal_system import Task, Pet, TaskType, Priority, Frequency, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session state initialization ──────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id="owner1",
        name="Jordan",
        time_available_minutes=120,
    )

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 0

if "task_counter" not in st.session_state:
    st.session_state.task_counter = 0

# ── Edit Owner Profile ────────────────────────────────────────────────────────

with st.expander("Edit owner profile"):
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name")
    with col_o2:
        time_available = st.number_input("Time available (minutes/day)", min_value=1, max_value=1440,
                                        value=st.session_state.owner.time_available_minutes, key="owner_time")

    prefs_input = st.text_input("Care preferences (comma-separated)", value=", ".join(st.session_state.owner.preferences), key="owner_prefs")

    if st.button("Save owner profile"):
        prefs = [p.strip() for p in prefs_input.split(",") if p.strip()]
        st.session_state.owner.edit(name=owner_name, time_available=time_available, preferences=prefs)
        st.success("Owner profile updated.")
        st.rerun()

# ── Add a Pet ─────────────────────────────────────────────────────────────────

st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="")

col4, col5 = st.columns(2)
with col4:
    age = st.number_input("Age (years)", min_value=0.0, max_value=30.0, value=1.0, step=0.5)
with col5:
    notes = st.text_input("Notes", value="")

if st.button("Add pet"):
    st.session_state.pet_counter += 1
    new_pet = Pet(
        pet_id=f"pet{st.session_state.pet_counter}",
        owner_id=st.session_state.owner.owner_id,
        name=pet_name,
        species=species,
        breed=breed,
        age_years=age,
        notes=notes,
    )
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {pet_name} to {st.session_state.owner.name}'s pets.")

pets = st.session_state.owner.pets
if pets:
    st.write(f"**{st.session_state.owner.name}'s pets:** " + ", ".join(p.name for p in pets))
    with st.expander("Edit a pet"):
        edit_pet_name = st.selectbox("Select pet to edit", [p.name for p in pets], key="edit_pet_select")
        edit_pet = next(p for p in pets if p.name == edit_pet_name)
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            new_name = st.text_input("Name", value=edit_pet.name, key="edit_pet_name")
        with col_e2:
            new_species = st.selectbox("Species", ["dog", "cat", "other"],
                                       index=["dog", "cat", "other"].index(edit_pet.species) if edit_pet.species in ["dog", "cat", "other"] else 2,
                                       key="edit_pet_species")
        with col_e3:
            new_breed = st.text_input("Breed", value=edit_pet.breed, key="edit_pet_breed")
        col_e4, col_e5 = st.columns(2)
        with col_e4:
            new_age = st.number_input("Age (years)", min_value=0.0, max_value=30.0, value=edit_pet.age_years, step=0.5, key="edit_pet_age")
        with col_e5:
            new_notes = st.text_input("Notes", value=edit_pet.notes, key="edit_pet_notes")
        if st.button("Save pet changes"):
            edit_pet.edit(name=new_name, species=new_species, breed=new_breed, age_years=new_age, notes=new_notes)
            st.success(f"Updated pet profile for {new_name}.")
            st.rerun()
    with st.expander("Delete a pet"):
        del_pet_name = st.selectbox("Select pet to delete", [p.name for p in pets], key="del_pet_select")
        del_pet = next(p for p in pets if p.name == del_pet_name)
        st.warning(f"This will remove {del_pet.name} and all their tasks.")
        if st.button("Delete pet", type="primary"):
            del_pet.delete(st.session_state.owner)
            st.success(f"Removed {del_pet_name}.")
            st.rerun()
else:
    st.info("No pets added yet.")

st.divider()

# ── Schedule a Task ───────────────────────────────────────────────────────────

st.subheader("Schedule a Task")

if not pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.name for p in pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in pets if p.name == selected_pet_name)

    col1, col2 = st.columns(2)
    with col1:
        task_type = st.selectbox(
            "Task type",
            options=list(TaskType),
            format_func=lambda t: t.value.replace("_", " ").title(),
        )
    with col2:
        priority = st.selectbox(
            "Priority",
            options=list(Priority),
            format_func=lambda p: p.value.title(),
        )

    col3, col4 = st.columns(2)
    with col3:
        start_hour = st.number_input("Start hour (0–23)", min_value=0, max_value=23, value=8)
        start_minute = st.number_input("Start minute", min_value=0, max_value=59, value=0, step=15)
    with col4:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox(
            "Frequency",
            options=list(Frequency),
            format_func=lambda f: f.value.title(),
        )

    description = st.text_input("Description", value="")

    if st.button("Add task"):
        st.session_state.task_counter += 1
        new_task = Task(
            task_id=f"task{st.session_state.task_counter}",
            pet_id=selected_pet.pet_id,
            task_type=task_type,
            start_time=datetime.time(int(start_hour), int(start_minute)),
            duration_minutes=int(duration),
            priority=priority,
            description=description,
            frequency=frequency,
        )
        new_task.add(selected_pet)
        st.success(f"Task '{task_type.value}' added to {selected_pet.name}.")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All scheduled tasks:**")
        st.table([
            {
                "Pet": next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id),
                "Type": t.task_type.value,
                "Start": str(t.start_time),
                "Duration": t.duration_minutes,
                "Priority": t.priority.value,
                "Description": t.description,
                "Done": t.is_completed,
            }
            for t in all_tasks
        ])
        with st.expander("Edit a task"):
            task_display = [f"{next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id)} - {t.task_type.value} @ {t.start_time}" for t in all_tasks]
            sel_task_display = st.selectbox("Select task to edit", task_display, key="edit_task_select")
            sel_task_idx = task_display.index(sel_task_display)
            sel_task = all_tasks[sel_task_idx]

            col_et1, col_et2 = st.columns(2)
            with col_et1:
                new_task_type = st.selectbox("Task type", list(TaskType),
                                            index=list(TaskType).index(sel_task.task_type),
                                            key="edit_task_type",
                                            format_func=lambda t: t.value.replace("_", " ").title())
            with col_et2:
                new_priority = st.selectbox("Priority", list(Priority),
                                           index=list(Priority).index(sel_task.priority),
                                           key="edit_task_priority",
                                           format_func=lambda p: p.value.title())

            col_et3, col_et4 = st.columns(2)
            with col_et3:
                new_start_hour = st.number_input("Start hour (0–23)", min_value=0, max_value=23,
                                                 value=sel_task.start_time.hour, key="edit_task_hour")
                new_start_minute = st.number_input("Start minute", min_value=0, max_value=59,
                                                   value=sel_task.start_time.minute, step=15, key="edit_task_minute")
            with col_et4:
                new_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240,
                                              value=sel_task.duration_minutes, key="edit_task_duration")

            new_freq = st.selectbox("Frequency", list(Frequency),
                                   index=list(Frequency).index(sel_task.frequency),
                                   key="edit_task_freq",
                                   format_func=lambda f: f.value.title())
            new_desc = st.text_input("Description", value=sel_task.description, key="edit_task_desc")

            if st.button("Save task changes"):
                sel_task.edit(
                    start_time=datetime.time(int(new_start_hour), int(new_start_minute)),
                    duration=int(new_duration),
                    priority=new_priority,
                    task_type=new_task_type,
                    description=new_desc,
                    frequency=new_freq
                )
                st.success(f"Updated task.")
                st.rerun()
        with st.expander("Delete a task"):
            task_display_del = [f"{next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id)} - {t.task_type.value} @ {t.start_time}" for t in all_tasks]
            sel_task_del_display = st.selectbox("Select task to delete", task_display_del, key="del_task_select")
            sel_task_del_idx = task_display_del.index(sel_task_del_display)
            sel_task_del = all_tasks[sel_task_del_idx]
            pet_of_task = next(p for p in pets if p.pet_id == sel_task_del.pet_id)

            st.warning(f"This will remove the task '{sel_task_del.task_type.value}' from {pet_of_task.name}.")
            if st.button("Delete task", type="primary", key="delete_task_btn"):
                sel_task_del.delete(pet_of_task)
                st.success(f"Removed task.")
                st.rerun()
        with st.expander("Mark task complete"):
            incomplete_tasks = [t for t in all_tasks if not t.is_completed]
            if incomplete_tasks:
                task_display_comp = [f"{next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id)} - {t.task_type.value} @ {t.start_time}" for t in incomplete_tasks]
                sel_task_comp_display = st.selectbox("Select task to mark complete", task_display_comp, key="comp_task_select")
                sel_task_comp_idx = task_display_comp.index(sel_task_comp_display)
                sel_task_comp = incomplete_tasks[sel_task_comp_idx]

                if st.button("Mark complete", key="complete_task_btn"):
                    next_task = sel_task_comp.complete()
                    if next_task:
                        sel_pet = next(p for p in pets if p.pet_id == sel_task_comp.pet_id)
                        next_task.add(sel_pet)
                        st.success(f"Marked complete. Next occurrence scheduled.")
                    else:
                        st.success(f"Marked complete.")
                    st.rerun()
            else:
                st.info("All tasks are already complete!")
    else:
        st.info("No tasks scheduled yet.")

st.divider()

# ── Filter Tasks ──────────────────────────────────────────────────────────────

st.subheader("Filter & View Tasks")

if st.session_state.owner.get_all_tasks():
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
    with col_f2:
        filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in pets])

    is_completed_filter = None
    if filter_status == "Completed":
        is_completed_filter = True
    elif filter_status == "Pending":
        is_completed_filter = False

    pet_name_filter = None if filter_pet == "All" else filter_pet

    filtered = st.session_state.owner.filter_tasks(is_completed=is_completed_filter, pet_name=pet_name_filter)

    if filtered:
        st.write(f"**Filtered tasks ({len(filtered)}):**")
        st.table([
            {
                "Pet": next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id),
                "Type": t.task_type.value,
                "Start": str(t.start_time),
                "Duration": t.duration_minutes,
                "Priority": t.priority.value,
                "Description": t.description,
                "Done": t.is_completed,
            }
            for t in filtered
        ])
    else:
        st.info("No tasks match the selected filters.")
else:
    st.info("No tasks scheduled yet.")

with st.expander("View pending tasks only"):
    pending = st.session_state.owner.get_all_pending_tasks()
    if pending:
        st.write(f"**Pending tasks ({len(pending)}):**")
        st.table([
            {
                "Pet": next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id),
                "Type": t.task_type.value,
                "Start": str(t.start_time),
                "Duration": t.duration_minutes,
                "Priority": t.priority.value,
                "Description": t.description,
            }
            for t in pending
        ])
    else:
        st.info("No pending tasks!")

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────

st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not pets:
        st.warning("Add at least one pet and task first.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule, warnings = st.session_state.owner.generate_schedule()
        st.text(schedule.summarize())
        for w in warnings:
            st.warning(w)

if st.session_state.owner.get_all_tasks() and pets:
    schedule, _ = st.session_state.owner.generate_schedule()

    with st.expander("View schedule by pet"):
        sel_pet_name = st.selectbox("Select pet", [p.name for p in pets], key="sched_pet_select")
        sel_pet = next(p for p in pets if p.name == sel_pet_name)
        pet_tasks = schedule.get_tasks_by_pet(sel_pet.pet_id)

        if pet_tasks:
            st.write(f"**Tasks for {sel_pet_name} ({len(pet_tasks)}):**")
            st.table([
                {
                    "Type": t.task_type.value,
                    "Start": str(t.start_time),
                    "Duration": t.duration_minutes,
                    "Priority": t.priority.value,
                    "Description": t.description,
                    "Done": t.is_completed,
                }
                for t in pet_tasks
            ])
        else:
            st.info(f"No tasks scheduled for {sel_pet_name}.")

    with st.expander("View schedule by task type"):
        sel_type = st.selectbox("Select task type", list(TaskType),
                               format_func=lambda t: t.value.replace("_", " ").title(),
                               key="sched_type_select")
        type_tasks = schedule.get_tasks_by_type(sel_type)

        if type_tasks:
            st.write(f"**{sel_type.value.replace('_', ' ').title()} tasks ({len(type_tasks)}):**")
            st.table([
                {
                    "Pet": next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id),
                    "Start": str(t.start_time),
                    "Duration": t.duration_minutes,
                    "Priority": t.priority.value,
                    "Description": t.description,
                    "Done": t.is_completed,
                }
                for t in type_tasks
            ])
        else:
            st.info(f"No {sel_type.value.replace('_', ' ').lower()} tasks scheduled.")

    with st.expander("View schedule by priority"):
        sel_priority = st.selectbox("Select priority", list(Priority),
                                   format_func=lambda p: p.value.title(),
                                   key="sched_priority_select")
        priority_tasks = schedule.get_tasks_by_priority(sel_priority)

        if priority_tasks:
            st.write(f"**{sel_priority.value.title()} priority tasks ({len(priority_tasks)}):**")
            st.table([
                {
                    "Pet": next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id),
                    "Type": t.task_type.value,
                    "Start": str(t.start_time),
                    "Duration": t.duration_minutes,
                    "Description": t.description,
                    "Done": t.is_completed,
                }
                for t in priority_tasks
            ])
        else:
            st.info(f"No {sel_priority.value.lower()} priority tasks scheduled.")

    with st.expander("Complete task from schedule"):
        incomplete_sched_tasks = [t for t in schedule.tasks if not t.is_completed]
        if incomplete_sched_tasks:
            task_display_sched = [f"{next((p.name for p in pets if p.pet_id == t.pet_id), t.pet_id)} - {t.task_type.value} @ {t.start_time}" for t in incomplete_sched_tasks]
            sel_sched_task_display = st.selectbox("Select task to mark complete", task_display_sched, key="sched_comp_select")
            sel_sched_task_idx = task_display_sched.index(sel_sched_task_display)
            sel_sched_task = incomplete_sched_tasks[sel_sched_task_idx]

            if st.button("Mark complete in schedule", key="sched_complete_btn"):
                next_task = schedule.complete_task(sel_sched_task)
                if next_task:
                    st.success(f"Marked complete. Next occurrence added to schedule.")
                else:
                    st.success(f"Marked complete.")
                st.rerun()
        else:
            st.info("All schedule tasks are complete!")
