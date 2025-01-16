from datetime import datetime, timedelta
from habit import Habit

def overview_habit(habit): #prints an overview of the habit
    habit.update_stats()
    print(f"Habit: \033[1m{habit.name}\033[0m")
    print(f"Description: {habit.description}")
    print(f"Periodicity: {"daily" if habit.periodicity == 1 else "weekly"}")
    print(f"Current Status: {'Broken' if habit.is_due() == "overdue" else 'Active Streak'}\n")

def details_habit(habit): #prints the details inkl. the dates of checks of a habit
    habit.update_stats()
    print(f"\nHabit: \033[1m{habit.name}\033[0m")
    print(f"Description: {habit.description}")
    print(f"Created: {habit.creation_date.strftime('%Y-%m-%d')}")
    print(f"Periodicity: {habit.periodicity} day(s)")
    print(f"---\nLongest streak: {habit.longest_streak}")
    print(f"Current streak: {habit.streak}")
    print(f"Broken: {habit.broken} time(s)")
    print(f"Success rate: {habit.success_rate:.2f}%")
    print(f"Successfull completions: {habit.successful_completions}")
    print(f"---\nList of completions:")
    if not habit.completions:
        print("No completions registered.")
    else:
        for completion in sorted(habit.completions,reverse=True):
            completion_date = completion.strftime('%Y-%m-%d, %H:%M h')
            print(f"- {completion_date}")

def get_struggling_habits(habits): #if there are habits that have been broken it returns a list of them
    if not habits:
        return None
    else:
        struggling = [habit for habit in habits if habit.broken>0]
        if not struggling:
            return None        
        else:
            sorted_struggling = sorted(struggling, key=lambda habit: habit.success_rate)
            return sorted_struggling

def get_habits_with_streak(habits): #if there are habits that already started a streak retruns a list of them
    if not habits:
        return None
    else:
        on_streak = [habit for habit in habits if habit.streak>0]
        if not on_streak:
            return None
        else:
            sorted_on_streak = sorted(on_streak, key=lambda habit: habit.longest_streak, reverse = True)
            return sorted_on_streak

def get_habit_longest_streak(habits): #If the list of habits is not empty, the habit(s) with the longest streak is returned.
    streak_habits = get_habits_with_streak(habits)
    if not streak_habits:
        return None
    else:
        max_longest_streak = max(habit.longest_streak for habit in streak_habits)
        habits_max_longest_streak = [habit for habit in streak_habits if habit.longest_streak == max_longest_streak]
        return habits_max_longest_streak
    
def get_habit_most_struggling(habits): #If the list of habits is not empty, the habit(s) with the lowest success rate is returned.
    struggling_habits = get_struggling_habits(habits)
    if not struggling_habits:
        return None
    else:
        min_success = min(habit.success_rate for habit in struggling_habits)
        habits_min_success = [habit for habit in struggling_habits if habit.success_rate == min_success]
        return habits_min_success