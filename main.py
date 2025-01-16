# import of classes and libraries
from manager import HabitManager
from analysis import overview_habit, details_habit, get_habits_with_streak, get_struggling_habits, get_habit_longest_streak, get_habit_most_struggling

#definition of the main loop for user interaction
def main():
    manager = HabitManager()

    #welcoming the user and providing an overview of the programm
    print(f"\n\033[1mWelcome\033[0m to \033[1;36mS\033[0mtreak\033[1;32mC\033[0mheck, \nyour personal habit tracker!")

    # loading the habits from json file, also displaying if there is no prior data
    manager.load_habits()
    
    #defining the total, daily and weekly habit lists
    habit_list = manager.habits

    #Main Menue
    while True:
        #List of options for the user
        print("\n--- \033[1;36mM\033[0main \033[1;32mM\033[0menu ---")
        if habit_list:  #if no prior data removes all options to manage them
            print("[1] Check my Habits")     #check-off a habit
            print("[2] Add/remove Habits")   #manage your habits new habit
            print("[3] Analyze my Habits")   #overview of all habits and their streaks
        else:
            print("[2] Add a Habit")
        print("[.] Save & Exit")             #save the habits to a file and exit the programm
        choice = input("___\nPlease, choose an option: ")
        
        #User input for the options
        if choice == "1":       #check-off a habit
            while True:
                print("\n-- \033[1;36mC\033[0mhecking off a \033[1;32mH\033[0mabit --\n")
                if not habit_list:
                    print("No habits available for check-off.")
                    break
                else:
                    sorted_habit_list = sorted(habit_list, key = lambda habit: habit.due_date)
                    for habit in sorted_habit_list:
                        print(f"\033[1m[{habit.name}]\033[0m ({habit.has_periodicity()}):", habit.is_due())
                    print("\n[.] Back to Main Menu")
                    name = input("____\nEnter the [name] of the Habit to check-off: ")
                    if name == ".":
                        break
                    else:
                        manager.complete_habit(name)

        elif choice == "2":     #manage my habits
            while True:
                print("\n-- \033[1;36mM\033[0managing my \033[1;32mH\033[0mabits --\n")
                if not habit_list:
                    print("Currently not habits are beeing tracked. Please start by adding one.")

                else:
                    sorted_habit_list = sorted(habit_list, key = lambda habit: habit.name)
                    for habit in sorted_habit_list:
                        print(f"\033[1m[{habit.name}]\033[0m ({"daily" if habit.periodicity == 1 else "weekly"})")
        
                print("___\n[1] Add a new Habit")
                if habit_list:
                    print("[2] Delete a Habit")
                print("[.] Back to Main Menu")
                manage_choice = input("___\nPlease, choose an option: ")

                if manage_choice == "1":
                    print("\n- \033[1;36mA\033[0mdding a new \033[1;32mH\033[0mabit -")
                    name = input("Enter a name for the habit: ")
                    if name == ".":
                        print("'.' is not a valid name. Please choose a different name.")
                        continue
                    elif manager.get_habit(name):
                            print(f"Habit '{name}' already exists. Please choose a different name.")
                    else:
                        description = input("Enter a description: ")
                        periodicity = input("Enter periodicity ([d]aily or [w]eekly): ")
                        if periodicity == "daily" or periodicity == "day" or periodicity == "d":
                            periodicity = 1
                            manager.add_habit(name, description, periodicity)
                        elif periodicity == "weekly" or periodicity == "week" or periodicity == "w":
                            periodicity = 7
                            manager.add_habit(name, description, periodicity)
                        else: 
                            print("Not a valid interval! Try again.")

                elif manage_choice == "2":
                    print("\n- \033[1;36mD\033[0melete an old \033[1;32mH\033[0mabit -\n")
                    if not habit_list:
                        print("No habits available to delete.")
                        continue
                    else:
                        name = input("Enter [name] of the habit to delete: ")
                        manager.remove_habit(name)
                
                elif manage_choice == ".":
                    break

                else:
                    print("Not a valid option. Try another one.")
        
        elif choice == "3":     #analyze the habits
            if not habit_list:
                print("\nNo habits available for analysis.")
                continue
            else:
                daily_habit_list = manager.get_daily_habits()
                weekly_habit_list = manager.get_weekly_habits()

                while True:
                    print("\n\n-- \033[1;36mA\033[0mnalyze my \033[1;32mH\033[0mabits --")
                    print("[1] Overview of all Habits")
                    print("[2] Longest Streak(s)")
                    print("[3] Struggling Habits")
                    print("[4] Details for a Habit")
                    print("[.] Back to Main Menu")
                    analysis_choice = input("___\nChoose an option: ")

                    if analysis_choice == "1":          #overview of all habits
                        print("\n- \033[1;36mO\033[0mverview daily \033[1;32mH\033[0mabits -")
                        if not daily_habit_list:
                            print("No daily habits available.")
                        else:
                            sorted_daily_habits = sorted(daily_habit_list, key=lambda habit: habit.name)
                            for i in range(0, len(sorted_daily_habits), 1):
                                overview_habit(sorted_daily_habits[i])

                        print("- \033[1;36mO\033[0mverview weekly \033[1;32mH\033[0mabits -") 
                        if not weekly_habit_list:
                            print("No weekly habits available.")
                            continue
                        else:
                            sorted_weekly_habits = sorted(weekly_habit_list, key=lambda habit: habit.name)
                            for i in range(0, len(sorted_weekly_habits), 1):
                                overview_habit(sorted_weekly_habits[i])

                    elif analysis_choice == "2":        #longest streak(s)
                        print("\n- \033[1;36mL\033[0mongest \033[1;32mS\033[0mtreak(s) -\n")
                        habits = get_habit_longest_streak(habit_list)
                        if not habits:
                            print("You have no habits with a recorded streak, yet.")
                        else:
                            print (f"All Habits:")
                            if len(habits) == 1:
                                for habit in habits:
                                    print(f"\033[1;32m'{habit.name}'\033[0m ({habit.has_periodicity()}) with {habit.longest_streak} consecutive timely completions (success rate: {habit.success_rate:.2f}%).")
                            else:
                                print("There is tie for the longest streak:")
                                for habit in habits:
                                    print(f"\033[1;32m'{habit.name}'\033[0m ({habit.has_periodicity()}) with {habit.longest_streak} consecutive timely completions ({habit.success_rate:.2f}%)")      
                            
                            print("\nDaily Habits (Ranking):")
                            ranked_daily_habits = get_habits_with_streak(daily_habit_list)
                            for i, habit in enumerate(ranked_daily_habits):
                                print(f"{i+1}. '{habit.name}' with a streak of {habit.longest_streak} timely completions (success rate: {habit.success_rate:.2f}%)")
                            
                            print("\nWeekly Habits (Ranking):")
                            ranked_weekly_habits = get_habits_with_streak(weekly_habit_list)
                            for i, habit in enumerate(ranked_weekly_habits):
                                print(f"{i+1}. '{habit.name}' with a streak of {habit.longest_streak} timely completions (success rate: {habit.success_rate:.2f}%)")
                                     
                    elif analysis_choice == "3":        #struggling habits
                        print("\n- \033[1;36mS\033[0mtruggling \033[1;32mH\033[0mabit(s) -\n")
                        habits = get_habit_most_struggling(habit_list)                       
                        if not habits:
                            print ("You have no 'struggling' habits. None of your tracked habit streaks ever broke.")
                        else:
                            print (f"All Habits:")
                            if len(habits) == 1:
                                for habit in habits:
                                    print(f"\033[1;31m'{habit.name}'\033[0m ({habit.has_periodicity()}) with {habit.broken} broken streaks is the habit you struggle the most with:\n Only {habit.success_rate:.2f}% of your completions were within.")
                            else:
                                print("There is tie for the habit you struggle the most with:")
                                for habit in habits:
                                    print(f"\033[1;31m'{habit.name}'\033[0m ({habit.has_periodicity()}) with {habit.broken} broken streaks is one of the habits you struggle the most with:\n Only {habit.success_rate:.2f}% of your completions were within.")

                            print("\nDaily Habits (Ranking):")
                            ranked_daily_habits = get_struggling_habits(daily_habit_list)
                            for i, habit in enumerate(ranked_daily_habits):
                                print(f"{i+1}. '{habit.name}' with {habit.broken} broken streaks and only {habit.success_rate:.2f}% timely completions")

                            print("\nDaily Habits (Ranking):")
                            ranked_weekly_habits = get_struggling_habits(weekly_habit_list)
                            for i, habit in enumerate(ranked_weekly_habits):
                                print(f"{i+1}. '{habit.name}' with {habit.broken} broken streaks and only {habit.success_rate:.2f}% timely completions")
                            
                
                    elif analysis_choice == "4":        #details for a habit
                        print("\n- \033[1;36mD\033[0metails for \033[1;32mH\033[0mabit -")
                        sorted_habit_list = sorted(habit_list, key=lambda habit: habit.name)
                        for habit in sorted_habit_list:
                            print(f"\033[1m[{habit.name}]\033[0m ({"daily" if habit.periodicity == 1 else "weekly"})")
                        print("\n[.] Back to Main Menu")
                        name = input("___\nEnter the [name] of the habit you want details on: ")
                        habit = manager.get_habit(name)
                        if name == ".":
                            continue
                        else:
                            if not habit:
                                print(f"Habit '{name}' not found.")   
                            else:
                                details_habit(habit)

                    elif analysis_choice == ".":        #back to main menu
                        break

                    else:
                        print("Not a valid option. Try another one.")
    
        elif choice == ".":     #save the habits to a file and exit the programm
            manager.save_habits()
            print("Thank you for using \033[1;36mS\033[0mtreak\033[1;32mC\033[0mheck. Goodbye!\n")
            break

        elif choice == "/":     #exit without saving [hidden option]
            break

        #if the user input is not valid
        else:
            print("Invalid option. Please try again.")

# start of the main loop
if __name__ == "__main__":
    main()