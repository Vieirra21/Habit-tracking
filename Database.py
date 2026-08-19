import sqlite3

class SimpleDatabase:
    def __init__(self, db_name="portfolio_habits.db"):
        # Connect to the database file
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Creates basic tables if they don't exist yet."""
        cursor = self.conn.cursor()
        
        # Table for habits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                periodicity TEXT
            )
        ''')
        
        # Table for checking off tasks (uses text for simple dates like "2026-08-19")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkoffs (
                habit_id INTEGER,
                check_date TEXT
            )
        ''')
        self.conn.commit()

    def add_habit(self, name: str, periodicity: str):
        """Saves a new habit and returns its new ID."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO habits (name, periodicity) VALUES (?, ?)", (name, periodicity))
        self.conn.commit()
        return cursor.lastrowid

    def check_off_habit(self, habit_id: int, date_string: str):
        """Saves a check-off date for a specific habit."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO checkoffs (habit_id, check_date) VALUES (?, ?)", (habit_id, date_string))
        self.conn.commit()

    def get_all_habits(self):
        """Returns all habits as a simple list of tuples."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, periodicity FROM habits")
        return cursor.fetchall()

    def get_dates_for_habit(self, habit_id: int):
        """Returns a list of date strings when the habit was completed."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT check_date FROM checkoffs WHERE habit_id = ? ORDER BY check_date ASC", (habit_id,))
        # Extracts just the date string from the database row
        return [row[0] for row in cursor.fetchall()]
    
    def delete_habit(self, habit_id: int):
        """Deletes a habit and all its check-offs from the database."""
        cursor = self.conn.cursor()
        
        # 1. Delete all check-offs associated with this habit
        cursor.execute("DELETE FROM checkoffs WHERE habit_id = ?", (habit_id,))
        
        # 2. Delete the habit itself
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        
        self.conn.commit()