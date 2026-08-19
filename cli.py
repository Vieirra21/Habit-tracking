from main import HabitTracker

def initialize_predefined_habits(tracker):
    """Checks if the database is empty and adds 5 default habits if so."""
    existing_habits = tracker.db.get_all_habits()
    
    if len(existing_habits) == 0:
        print("Database is empty. Inserting 5 pre-defined habits...\n")
        tracker.create_new_habit("Drink 2 Liters of Water", "daily")
        tracker.create_new_habit("Read 15 Pages", "daily")
        tracker.create_new_habit("Exercise for 30 Minutes", "daily")
        tracker.create_new_habit("Practice Python Coding", "daily")
        tracker.create_new_habit("Meal Prep for the Week", "weekly")
        print("-" * 30)

def display_menu():
    """Prints the main menu options to the screen."""
    print("\n=== HABIT TRACKER MENU ===")
    print("1. View all habits")
    print("2. Enter a new habit")
    print("3. Check off a habit (Complete a task)")
    print("4. View Analytics")
    print("5. Delete a habit")
    print("6. Exit Application")
    print("==========================")

def run_app():
    """The main loop that runs the interactive application."""
    tracker = HabitTracker()
    initialize_predefined_habits(tracker)
    
    while True:
        display_menu()
        choice = input("Please select an option (1-6): ")
        
        if choice == '1':
            print("\n--- Your Habits ---")
            habits = tracker.db.get_all_habits()
            for habit in habits:
                habit_id, name, periodicity = habit
                print(f"ID {habit_id}: {name} ({periodicity})")
                
        elif choice == '2':
            print("\n--- Create New Habit ---")
            name = input("What is the name of the new habit? ")
            periodicity = input("Is this habit 'daily' or 'weekly'? ")
            tracker.create_new_habit(name, periodicity)
            
        elif choice == '3':
            print("\n--- Check Off Habit ---")
            habits = tracker.db.get_all_habits()
            for habit in habits:
                print(f"ID {habit[0]}: {habit[1]}")
                
            habit_id_str = input("\nEnter the ID of the habit you completed: ")
            
            try:
                habit_id = int(habit_id_str)
                tracker.complete_habit(habit_id) 
            except ValueError:
                print("Invalid input. Please enter the numerical ID.")
                
        elif choice == '4':
            print("\n--- Your Analytics ---")
            print("Daily Habits:", tracker.get_daily_habits())
            print("Longest Streak Overall:", tracker.get_longest_streak_overall(), "days")
            print("Habit struggled with most:", tracker.get_most_struggled_habit())
            
        elif choice == '5':
            print("\n--- Delete a Habit ---")
            habits = tracker.db.get_all_habits()
            for habit in habits:
                print(f"ID {habit[0]}: {habit[1]}")
                
            habit_id_str = input("\nEnter the ID of the habit you want to delete: ")
            
            try:
                habit_id = int(habit_id_str)
                tracker.delete_habit(habit_id)
            except ValueError:
                print("Invalid input. Please enter the numerical ID.")
                
        elif choice == '6':
            print("\nExiting Habit Tracker. Keep up the good work!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    run_app()