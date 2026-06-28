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
    else:
        st.info("No tasks scheduled yet.")

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
