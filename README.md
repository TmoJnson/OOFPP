# README for StreakCheck

Welcome to Streak_Check, your personal habit tracker! This program helps you manage and analyze your habits to stay consistent and achieve your goals. Below, you will find step-by-step instructions on how to use the program effectively.

## 1. Getting Started

### Requirements
- Interpreter with Python 3.7 or higher
- pytest

### Launch the Program:
Run the program by executing the main.py file in an interpreter of your choice: 
<code>python main.py</code>
<br>You will be greeted with a welcome message.

### Load Habits:

If you have previously saved habits, the program will automatically load them. Otherwise, you start with a fresh habit tracker by adding your habits.

## 2. Main Menu Options

After starting the program, the main menu will appear with the following options:

### <code>[1] Check My Habits</code>

Select this option to mark habits as completed. StreakCheck shows you a list of your <code>[Habits]</code> and their due date, sorted by their priority. So the Habits that need completion the earliest appear first.

#### Instructions:

Choose a habit to be completed by entering its <code>[name]</code> and confirming your choice by hitting <kbd>Enter</kbd> (The input is <ins>not</ins> case sensitive). If you enter a name matching the list and you have not already completed the task earlier the same day, your Habit will be checked-off and you get feedback whether you completed it on time and continued your streak or you broke.

Keep checking off your completed Habits. If you want to return to the main menue enter: <code>.</code> + <kbd>Enter</kbd>

### <code>[2] Add/Remove Habits</code>

Use this menu to manage your list of habits. StreakCheck shows you your currently tracked habits in alphabetical order.
|Options| Instructions|
|-|-|
|<code>[1] Add a Habit|- Enter a unique name for the habit.<br>- Provide a description.<br>- Specify the periodicity as daily (<code>d</code>) or weekly (<code>w</code>).<br>- If every input is valid you get a confirmation.|
| <code>[2] Delete a Habit</code> |- Enter the name of the habit you wish to delete.<br> - The habit will be removed permanently. So please, be sure.<br>- If your input matches a Habit, you get a confirmation.|
|<code>[.] Back to Main Menu</code>|Return to the main menu by entering <code>.</code>|
|||

### <code>[3] Analyse My Habits</code>

Get insights into your habits.

|Options| Explanation / Instructions|
|-|-|
|<code>[1] Overview of all Habits</code>|Displays a summary of your daily and weekly habits.|
|<code>[2] Longest Streak(s)|Shows the habit with the longest streak and rankings for daily and weekly habits.|
|<code>[3] Struggling Habits | Highlights habits that are frequently incomplete or overdue.|
|<code>[4] Details for a Habit |- Enter the name of a habit from the provided list, to see detailed statistics.|
|<code>[.] Back to Main Menu</code> | Return to the main menu by entering <code>.</code>|
|||

### <code> [4] Save & Exit</code>
Save your progress and exit the application.
All habit data will be stored in a JSON file called <code>habits.json</code> for future use.


### Additional / Hidden Features:
|||
|-|-|
|Input Validation|Invalid inputs (e.g., duplicate names, unrecognized periodicity) will prompt error messages.|
|Back one Menu level|  Enter <code>.</code> at any input prompt.|
|Exit without saving|Enter <kbd>/</kbd> at the main menu. All changes within the session will be undone|
|||

## 3. Tips for Effective Usage

1. Start small: Add only a few habits at first and gradually expand your list.

2. Be consistent: Check off your habits daily or weekly to maintain streaks.

3. Review analytics: Use the analysis tools to identify your strengths and areas for improvement.

##  Thank you for using **StreakCheck**! <br>Stay consistent and achieve your goals.
