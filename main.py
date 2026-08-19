import datetime
from Database import SimpleDatabase

class HabitTracker:
    def __init__(self):
        # Initialize our simplified database
        self.db = SimpleDatabase()

    def create_new_habit(self, name: str, periodicity: str):
        """Creates a habit directly in the database."""
        habit_id = self.db.add_habit(name, periodicity.lower())
        print(f"Created habit: {name} (ID: {habit_id})")
        return habit_id

    def complete_habit(self, habit_id: int, date_string: str = None):
        """Checks off a habit. Uses today's date if none is provided."""
        if date_string is None:
            # Gets today's date in a simple "YYYY-MM-DD" format
            date_string = datetime.date.today().strftime("%Y-%m-%d")
            
        self.db.check_off_habit(habit_id, date_string)
        print(f"Checked off habit ID {habit_id} on {date_string}")

    def delete_habit(self, habit_id: int):
        """Deletes a habit from the database."""
        self.db.delete_habit(habit_id)
        print(f"Habit ID {habit_id} has been successfully deleted.")

    # --- Analytics Methods ---

    def get_daily_habits(self):
        """Analytic 1: Returns a list of habits that are 'daily'."""
        all_habits = self.db.get_all_habits()
        daily_habits = []
        
        # A simple, readable loop
        for habit in all_habits:
            habit_id, name, periodicity = habit
            if periodicity == "daily":
                daily_habits.append(name)
                
        return daily_habits

    def calculate_streak(self, habit_id: int):
        """Calculates the longest streak for a specific habit."""
        dates = self.db.get_dates_for_habit(habit_id)
        
        if len(dates) == 0:
            return 0
            
        longest_streak = 1
        current_streak = 1
        
        # Convert text dates back to date objects just for the math
        date_objects = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
        
        # Loop through the dates and see if they are 1 day apart
        for i in range(1, len(date_objects)):
            # Calculate the difference in days between this check-off and the previous one
            days_apart = (date_objects[i] - date_objects[i-1]).days
            
            if days_apart == 1:
                # They are consecutive! Increase the streak.
                current_streak += 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
            elif days_apart > 1:
                # Missed a day, streak broken. Reset to 1.
                current_streak = 1
                
        return longest_streak

    def get_longest_streak_overall(self):
        """Analytic 2: Finds the longest streak among all habits."""
        all_habits = self.db.get_all_habits()
        best_overall_streak = 0
        
        for habit in all_habits:
            habit_id = habit[0]
            streak = self.calculate_streak(habit_id)
            if streak > best_overall_streak:
                best_overall_streak = streak
                
        return best_overall_streak

    def get_most_struggled_habit(self):
        """Analytic 3: Finds the habit with the fewest check-offs."""
        all_habits = self.db.get_all_habits()
        
        if not all_habits:
            return "No habits exist."

        struggled_habit_name = ""
        fewest_checkoffs = 9999 # Start with an artificially high number
        
        for habit in all_habits:
            habit_id, name, periodicity = habit
            
            # Count how many times this habit was checked off
            checkoffs = len(self.db.get_dates_for_habit(habit_id))
            
            if checkoffs < fewest_checkoffs:
                fewest_checkoffs = checkoffs
                struggled_habit_name = name
                
        return struggled_habit_name


if __name__ == "__main__":
    tracker = HabitTracker()
    
    # 1. Create some habits (Comment these out after running it the first time!)
    # workout_id = tracker.create_new_habit("Workout", "daily")
    # water_id = tracker.create_new_habit("Drink Water", "daily")
    
    # 2. Simulate checking them off over a few days
    # tracker.complete_habit(workout_id, "2026-08-15")
    # tracker.complete_habit(workout_id, "2026-08-16")
    # tracker.complete_habit(workout_id, "2026-08-17") # 3-day streak!
    
    # tracker.complete_habit(water_id, "2026-08-15") # Only did this once (struggled)

    # 3. Print the Analytics
    print("\n--- Analytics Results ---")
    print("Daily Habits:", tracker.get_daily_habits())
    print("Longest Streak Overall:", tracker.get_longest_streak_overall(), "days")
    print("Habit I struggled with most:", tracker.get_most_struggled_habit())