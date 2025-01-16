from datetime import datetime, timedelta

class Habit:
    #attributes
    def __init__(self, name, description, periodicity):
        """
        Creates a new habit instance with the given name, description, and periodicity.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity  # in days
        self.longest_streak = 0
        self.streak = 0
        self.broken = 0
        self.successful_completions = 0
        self.success_rate = 0
        self.due_date = 0
        self.creation_date = datetime.now()
        self.completions = [] #datetime
    
    #methods    
    def completed(self): #check if already checked. if not appends datetime.
        now = datetime.now()
        today = now.date()
        if self.completions and self.completions[-1].date() == today:  #checks whether is already checked-off today
            return False
        else:       #if not, the habit is checked off by appending the date to the list and updating the streak attributes of the habit instance
            self.completions.append(now)
            if self.update_stats() == True:
                return True
            else:
                print(f"Check-off for Habit '{self.name}' too late. Start a new streak.")
                return True
            
    def update_stats(self): #updates all stats of the habit instance
        if len(self.completions) == 1:
            self.longest_streak = 1
            self.streak = 1
            self.due_date = self.completions[-1] + timedelta(days=self.periodicity)
            return
        else:
            self.streak = self.calc_streak()
            self.broken = self.calc_broken()
            self.longest_streak = self.calc_longest_streak()
            self.successful_completions = self.calc_successful_completions()
            self.success_rate = self.calc_success_rate()
            self.due_date =  self.calc_due_date()
            if len(self.completions) >= 2 and self.completions[-1].date() - self.completions[-2].date() > timedelta(days=self.periodicity):
                return False
            else: return True

    def calc_streak(self): #Calculates and returns the current streak of a habit.
        if not self.completions:
            return 0
        else:
            sorted_completions = sorted(self.completions)
            current_streak = 1 
            for i in range(len(sorted_completions) - 1, 0, -1):
                if (sorted_completions[i].date() - sorted_completions[i - 1].date()).days <= self.periodicity:
                    current_streak += 1
                else:
                    break
            return current_streak
    
    def calc_broken(self): #Calculates and returns the number of broken streaks of a habit.
        if not self.completions:
            return 0
        else:
            sorted_completions = sorted(self.completions)
            broken = 0
            for i in range(len(sorted_completions) - 1, 0, -1):
                if (sorted_completions[i].date() - sorted_completions[i - 1].date()).days > self.periodicity:
                    broken += 1
            return broken

    def calc_longest_streak(self): #Calculates and return the longest streak of a habit.
        if not self.completions:
            return 0
        streaks = []
        sorted_completions = sorted(self.completions)
        current_streak = 1
        for i in range(0,len(sorted_completions)-1, 1):
            if sorted_completions[i+1].date() - sorted_completions[i].date() <= timedelta(days=self.periodicity):
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1
        # Add the final streak
        streaks.append(current_streak)
        return max(streaks)
    
    def calc_successful_completions(self): #Calcutes and returns successful completions of a habit
        if not self.completions:
            return 0
        else:
            successful_completion = 1
            sorted_completions = sorted(self.completions)
            for i in range(len(sorted_completions)-1, 0, -1):
                if sorted_completions[i].date() - sorted_completions[i-1].date() <= timedelta(days=self.periodicity):
                    successful_completion += 1
            self.successful_completions = successful_completion
            return successful_completion

    def calc_due_date(self): #calculates the due_date for a given habit
        last_check_date = self.completions[-1].date() if self.completions else self.creation_date.date()
        return last_check_date + timedelta(days=self.periodicity)

    def calc_success_rate(self): #calculates the success rate for a given habit
        total_completions = len(self.completions)
        if total_completions == 0:
            return 0
        else:
            success_rate = (self.successful_completions / total_completions) * 100
            return success_rate

    def is_due(self):   #calculates the remaining time to the due date for the next periodic check
        today_date = datetime.now().date()
        due_date = self.calc_due_date()
        time_left = due_date - today_date
        if time_left.days < 0:
            return "overdue"
        elif time_left.days == 0:
            return "due today"
        elif time_left.days == 1:
            return "due tomorrow"
        else:
            return f"due in {time_left.days} days"
    
    def has_periodicity(self):
        if self.periodicity == 1:
            return "daily"
        else: return "weekly"

    #methods to (de)serialize the Habit objects
    def to_dict(self): #transforms the habit instance into a dictionary for saving to a file
        return {
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date.isoformat(),
            "completions": [datetime.isoformat() for datetime in self.completions]
        }

    @staticmethod   #transforms a dictionary from a file back into a habit instance
    def from_dict(data):
        habit = Habit(data["name"], data["description"], data["periodicity"])
        habit.creation_date = datetime.fromisoformat(data["creation_date"])
        habit.completions = [datetime.fromisoformat(date) for date in data["completions"]]
        habit.streak = habit.calc_streak()
        habit.broken = habit.calc_broken()
        habit.longest_streak = habit.calc_longest_streak()
        habit.successful_completions = habit.calc_successful_completions()
        habit.due_date = habit.calc_due_date()
        habit.success_rate = habit.calc_success_rate()
        return habit