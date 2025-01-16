from habit import Habit
from storage import HabitStorage

class HabitManager:
    def __init__(self):
        self.habits = [] #List for the instances of class 'Habit'

    def add_habit(self, name, description, periodicity): #creates a Habit instance
        habit = Habit(name, description, periodicity)
        self.habits.append(habit)
        print(f"____\nAdded habit \033[1m'{name}'\033[0m with periodicity of {periodicity} days.")

    def remove_habit(self, name): #deletes instance if found
        if name == ".": return
        else:
            habit = self.get_habit(name)
            if not habit:
                print(f"Habit '{name}' not found.") 
            else:
                self.habits.remove(habit)
                print(f"Deleted Habit \033[1m'{name}'\033[0m and all its data.")

    def complete_habit(self, name): #Tries to get the habit instance with the given name. \
        #If the habit instance is found, the habit.completed() method is called to check, \
        #if the habit is not already checked off today, and if not, the habit is checked off.
        habit = self.get_habit(name)
        if not habit:
            print(f"Habit '{name}' not found.")
        else:
            if habit.completed():
                print(f"Habit '{name}' checked off. \nYou are on a streak of {habit.streak} timely completions.")
            else: print(f"Habit '{name}' already checked off today.")

    def get_habit(self, name): #Tries to get the habit instance with the given name.
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return habit
        return None

    def get_daily_habits(self): #Retuns a list with all daily habits
        daily_habits = [habit for habit in self.habits if habit.periodicity == 1]
        return daily_habits
    
    def get_weekly_habits(self): #Returns a list with all weekly habits
        weekly_habits = [habit for habit in self.habits if habit.periodicity == 7]
        return weekly_habits

# saving and loading the habits
    def save_habits(self) -> None:    #Calls the save_to_file() method of the HabitStorage class to save the list of habits to a file.
        HabitStorage().save_to_file(self.habits)

    def load_habits(self) -> None: #Calls the load_from_file() method of the habitStorage class to load the list of habits from a file.
        self.habits = HabitStorage().load_from_file()