# Habit Tracker App

## Introduction
The habit tracker app is a python-based project designed so the user can easily manage, track and analyze theire habits.
The goal of the app is to help people build new habits and routins and show their progress.

## Features

Register new account or login to start the app
create new habits 
View all your habits and inspect them for details
mark habits as complete and build streaks on them 
edit or remove habits
Analyze your habits with your build streaks and other stats
save your progress in a local database

## Requirements

Python 3.7 or later

`sqlite3` module 

`datetime` module 

`time` module

## Usage 

1. Clone the repository:
   ```bash
   git clone https://github.com/LeandroLuchtenberg/Habit_Tracker.git
   ```
  
3. open the directory
   ```bash
   cd Habit_Tracker
   ```
   
5. Strart the app
   ```bash
   python main.py
   ```
6. Register or Login:
    ```bash
   register: give your name and Password
   ```
     or
   ```bash
   Login: it comes with a test Account
   Username: Test
   Passwort: Test
    ```

8. follow the menu to:
   
   - show all habits and inspect certain ones closer
   - check off habits
   - analyze your habits
   - create, edit or remove Habits  
   - save your changes
   

## Example 

```
  What do you want to do?
   1. Show habits 
   2. complete habit 
   3. analyse habits
   4. add habit 
   5. edit habit 
   6. remove habit 
   7. close App
```


## Testing
The app includes a `unittest` located in `test.py`. It checks the validility of the core features of the app:

```bash
python -m unittest test.py
```

### Tested Features:
- registering 
- Login and Loading of data
- creating new habits
- edit habits 
- complete habits 
- analytics module
