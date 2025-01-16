import pytest                               # type: ignore
from datetime import datetime, timedelta   
from habit import Habit
from storage import HabitStorage
from manager import HabitManager
from analysis import get_habit_longest_streak, get_habits_with_streak, get_struggling_habits, get_habit_most_struggling

class TestStreakCheck:

    def setup_method(self): #Setup for the tests
        self.storage = HabitStorage()
        self.manager = HabitManager()
        self.storage.filedirect = "test.json"
        self.manager.add_habit("test_daily", "test_daily description", 1)
        self.manager.add_habit("test_weekly", "test_weekly description", 7)
        self.manager.complete_habit("test_daily")
        self.storage.save_to_file(self.manager.habits)

    def test_habit(self): #Test the methods of habit
        habit = Habit("test_habit_1", "test_description", 1)
        
        # Test completion
        habit.completed()
        assert len(habit.completions) == 1
        assert habit.streak > 0
        
        # Test calculations with single completion
        assert habit.calc_streak() == 1
        assert habit.calc_broken() == 0
        assert habit.calc_successful_completions() == 1
        assert habit.calc_success_rate() == 100 #%

        #test a datetime list with 4 elements of which 3 are timely and the last one is not
        habit.completions = [datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=5),datetime.now()-timedelta(days=3), datetime.now()]
        assert len(habit.completions) == 4
        assert habit.calc_streak() == 1
        assert habit.calc_broken() == 1
        assert habit.calc_longest_streak() == 3
        assert habit.calc_successful_completions() == 3
        assert habit.calc_success_rate() == 75 # %
        
        # Test due status
        assert habit.is_due() == "due tomorrow"
        
        # Test serialization and deserialization
        data = habit.to_dict()
        restored_habit = Habit.from_dict(data)
        assert restored_habit.name == habit.name
        assert restored_habit.description == habit.description
        assert restored_habit.creation_date == habit.creation_date
        assert restored_habit.completions == habit.completions

    def test_manager(self): # Test the methods of the manager
        # loading the habits from the storage
        self.manager.habits = self.storage.load_from_file()
        test_list = self.manager.habits
        assert len(test_list) == 2  # Check that the two habits were loaded
        
        # Test completing habits
        self.manager.complete_habit("test_daily")
        self.manager.complete_habit("test_weekly")
        assert len(test_list) == 2
        assert len(test_list[0].completions) > 0
        assert len(test_list[1].completions) > 0
        self.storage.save_to_file(self.manager.habits)
        
        # Test adding and removing habits
        self.manager.add_habit("dummy", "dummy_description", 1)
        assert any(habit.name == "dummy" for habit in test_list)
        self.manager.remove_habit("dummy")
        assert not any(habit.name == "dummy" for habit in test_list)

    def test_storage(self): #Test the methods of storage
        pass
        habit1 = Habit("habit1","description 1", 1)
        habit1.completed()
        assert len(habit1.completions) == 1
        habit2 = Habit("habit2","description 2", 7)
        assert len(habit2.completions) == 0
        
        habits = [habit1, habit2]

        self.storage.save_to_file(habits) #dump to JSON
        habits_returned = self.storage.load_from_file()
        assert len(habits_returned) == 2
        assert habits_returned[0].name == "habit1"
        assert habits_returned[1].name == "habit2"
        assert len(habits_returned[0].completions) == 1
        assert len(habits_returned[1].completions) == 0
        

        #self.manager.habits = 

    def test_get_habit_with_streak(self): #test the analyses function
        #setup with 3 habits, 2 have a streak, the third has not yet been completed
        habit1 = Habit("habit_1", "Description 1", 1)
        habit1.completions = [datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=5), datetime.now()] #longest_streak = 2
        habit1.update_stats()

        habit2 = Habit("habit_2", "Description 2", 7)
        habit2.completions = [datetime.now()-timedelta(days=21), datetime.now()-timedelta(days=16),datetime.now()-timedelta(days=10),datetime.now()] #streak = 3
        habit2.update_stats()

        habit3 = Habit("habit_3", "Description 3", 1)
        habit3.update_stats()

        habits = [habit1, habit2, habit3]
        
        # Test with one habit with longest streak
        habits_with_streak = get_habits_with_streak(habits)
        assert len(habits_with_streak) == 2
        assert habits_with_streak[0] == habit2 #longest streak == 3 

        # Test with empty list
        habits_with_streak = get_habits_with_streak([])
        assert habits_with_streak is None

    def test_get_habit_longest_streak(self): #test the analyses function
        habit1 = Habit("habit_1", "Description 1", 1)
        habit1.completions = [datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=5), datetime.now()] #longest_streak = 2
        habit1.update_stats()

        habit2 = Habit("habit_2", "Description 2", 7)
        habit2.completions = [datetime.now()-timedelta(days=21), datetime.now()-timedelta(days=16),datetime.now()-timedelta(days=10),datetime.now()] #streak = 3
        habit2.update_stats()

        habits = [habit1, habit2]
        
        # Test with one habit with longest streak
        longest_streak_habit = get_habit_longest_streak(habits)
        print(longest_streak_habit)
        assert habit2 in longest_streak_habit  # Assuming habit2 is in the list with the longest streak

        habit1.completions = [datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=5),datetime.now()-timedelta(days=3),datetime.now()] #longest_streak = 3
        habit1.update_stats()

        # Test with both habits having the longest streak (==3)
        longest_streak_habit = get_habit_longest_streak(habits)
        assert habit2 in longest_streak_habit  # Assuming habit1 and habit2 is in the list with the longest streak
        assert habit1 in longest_streak_habit

        # Test with empty list
        longest_streak_habit = get_habit_longest_streak([])
        assert longest_streak_habit is None

    def test_get_struggling_habits(self): #test of this function
        #setup with 3 habits, 2 have 1 broken streak, the third has not yet been completed and broken, 
        habit1 = Habit("habit_1", "Description 1", 1)
        habit1.completions = [datetime.now()-timedelta(days=5), datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=3), datetime.now()] #success_rate = 75
        habit1.update_stats()

        habit2 = Habit("habit_2", "Description 2", 7)
        habit2.completions = [datetime.now()-timedelta(days=21), datetime.now()-timedelta(days=16), datetime.now()] #success_rate = 66.666
        habit2.update_stats()

        habit3 = Habit("habit_3", "Description 3", 1)
        habit3.update_stats()

        habits = [habit1, habit2, habit3]
        
        # Test with one habit with longest streak
        habits_with_streak = get_struggling_habits(habits)
        assert len(habits_with_streak) == 2
        assert habits_with_streak[0] == habit2 #lower success_rate 

        # Test with empty list
        habits_with_streak = get_struggling_habits([])
        assert habits_with_streak is None

    def test_get_habit_most_struggling(self): #Test of this function
        #setup with 3 habits, 2 have 1 broken streak, the third has not yet been completed and broken, 
        habit1 = Habit("habit_1", "Description 1", 1)
        habit1.completions = [datetime.now()-timedelta(days=5), datetime.now()-timedelta(days=4), datetime.now()-timedelta(days=3), datetime.now()] #success_rate = 75
        habit1.update_stats()

        habit2 = Habit("habit_2", "Description 2", 7)
        habit2.completions = [datetime.now()-timedelta(days=21), datetime.now()-timedelta(days=16), datetime.now()] #success_rate = 66.666
        habit2.update_stats()

        habit3 = Habit("habit_3", "Description 3", 1)
        habit3.update_stats()

        habits = [habit1, habit2, habit3]

        #Test with single most struggling (min: success_rate)
        habits_most_struggling = get_habit_most_struggling(habits)
        assert len(habits_most_struggling) == 1
        assert habit2 in habits_most_struggling #because of lowest success_rate

        #Test with a tie betweeen habit1 and habit2
        habit2.completions = [datetime.now()-timedelta(days=21), datetime.now()-timedelta(days=16), datetime.now()-timedelta(days=10), datetime.now()] #success_rate = 75
        habit2.update_stats()

        habits_most_struggling = get_habit_most_struggling(habits)
        assert len(habits_most_struggling) == 2
        assert habit1 in habits_most_struggling
        assert habit2 in habits_most_struggling

    def teardown_method(self): #teardown of test setup JSON
        import os
        if os.path.exists("test.json"):
            os.remove("test.json")