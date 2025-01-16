import pytest                               # type: ignore
from datetime import datetime, timedelta   
from habit import Habit
from storage import HabitStorage
from manager import HabitManager
from analysis import get_habit_longest_streak

class TestTracker:

    def setup_method(self):
        self.storage = HabitStorage()
        self.manager = HabitManager()
        self.storage.filedirect = "test.json"
        self.manager.add_habit("test_daily", "test_daily description", 1)
        self.manager.add_habit("test_weekly", "test_weekly description", 7)
        self.manager.complete_habit("test_daily")
        self.storage.save_to_file(self.manager.habits)

    def test_habit(self):
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

    def test_manager(self):
        # Test loading habits
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

    def test_get_habit_longest_streak(self):
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
    
    def teardown_method(self):
        import os
        if os.path.exists("test.json"):
            os.remove("test.json")
