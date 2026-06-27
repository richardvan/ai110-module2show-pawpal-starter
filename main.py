from pawpal_system import TaskType, Priority, Frequency, Task, Pet, Schedule, Owner

my_pet01 = Pet(pet_id="pet1", 
               name="Buddy", 
               owner_id="owner1", 
               species="Dog", 
               breed="Golden Retriever", 
               age_years=3.5, 
               notes="Friendly and energetic.", 
               tasks=[]
               )
my_pet02 = Pet(pet_id="pet2", 
               name="Max", 
               owner_id="owner1", 
               species="Dog", 
               breed="Labrador Retriever", 
               age_years=2.0, 
               notes="Playful and loyal.", 
               tasks=[]
               )


import datetime

task1 = Task(task_id="task1", pet_id="pet1", task_type=TaskType.WALK_PET,
             start_time=datetime.time(7, 0), duration_minutes=30,
             priority=Priority.HIGH, description="Morning walk", frequency=Frequency.DAILY)
task2 = Task(task_id="task2", pet_id="pet1", task_type=TaskType.FEED_FOOD,
             start_time=datetime.time(8, 0), duration_minutes=10,
             priority=Priority.HIGH, description="Breakfast", frequency=Frequency.DAILY)
task3 = Task(task_id="task3", pet_id="pet1", task_type=TaskType.GROOM,
             start_time=datetime.time(17, 0), duration_minutes=20,
             priority=Priority.LOW, description="Brush coat", frequency=Frequency.WEEKLY)

task4 = Task(task_id="task4", pet_id="pet2", task_type=TaskType.WALK_PET,
             start_time=datetime.time(7, 30), duration_minutes=30,
             priority=Priority.HIGH, description="Morning walk", frequency=Frequency.DAILY)
task5 = Task(task_id="task5", pet_id="pet2", task_type=TaskType.FEED_FOOD,
             start_time=datetime.time(8, 30), duration_minutes=10,
             priority=Priority.HIGH, description="Breakfast", frequency=Frequency.DAILY)
task6 = Task(task_id="task6", pet_id="pet2", task_type=TaskType.PROVIDE_ENRICHMENT,
             start_time=datetime.time(16, 0), duration_minutes=15,
             priority=Priority.MEDIUM, description="Fetch and play session", frequency=Frequency.DAILY)

my_pet01.tasks = [task1, task2, task3]
my_pet02.tasks = [task4, task5, task6]

my_owner = Owner(owner_id="owner1", name="John Doe", time_available_minutes=120)
my_owner.add_pet(my_pet01)
my_owner.add_pet(my_pet02)

schedule = my_owner.generate_schedule()
print("Today's Schedule")
print(schedule.summarize())
