import json
from habit import Habit

class HabitStorage:
    def __init__(self):
        self.filedirect = "habits.json"
    
    def save_to_file(self, habits): #writes the dicts with habit instances to a json file.
        try:
            with open(self.filedirect, 'w') as file:
                json.dump([habit.to_dict() for habit in habits], file, indent=4)
            print(f"Habits successfully saved to {self.filedirect}.")
        except Exception as e:
            print(f"Error saving habits: {e}")

    def load_from_file(self): #Reads the habit data from a json file and returns a list of Habit instances.
        try:
            with open(self.filedirect, 'r') as file:
                habit_dicts = json.load(file)                               #loads the json file into a list of dictionaries
                return [Habit.from_dict(habit) for habit in habit_dicts]    #for each dictionary in the list, a habit instance is created using the from_dict() method and appended to a list of habits
        except FileNotFoundError:
            print(f"\n\033[1mNo prior user data found (file: {self.filedirect}).\n\033[0m\nStarting with an empty habit tracker.")
            return []
        except Exception as e:
            print(f"Error loading habits: {e}")
            return []