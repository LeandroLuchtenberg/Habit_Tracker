import time
import datetime
import sqlite3
from time import sleep
import analyse
from habit import Habit


class Habit_Tracker():
    """Main Habit Tracker class """
    def __init__(self, db):
        """initializes the habit tracker wit connection to db"""
        self.conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES |
                                                         sqlite3.PARSE_COLNAMES)

        self.cur = self.conn.cursor()

        #self.cur.execute("DROP TABLE habits")
        #self.cur.execute("DROP TABLE user")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        user(user_id INTEGER PRIMARY KEY, name TEXT, password TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        habits(habit_id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency INTEGER, specification TEXT, state INTEGER, streak INTEGER, history INTEGER, longest_streak INTEGER,last_done TEXT, last_check TEXT,created TEXT,completion_dates TEXT, fulfilled INTEGER, failed INTEGER, FOREIGN KEY(user_id) REFERENCES user(user_id))""")

        # cur.execute("INSERT INTO user VALUES (0, 'a','s')")

        self.habit_list = []
        self.id_list = []


    def get_habit_list(self):
        return self.habit_list

    def create_habit(self, name = "", frequency = None, specification =""):
        """
        creating habit with user inputs for name and frequency
        """
        if name == "":
            name = input("Enter the name:\n")
        if frequency == None:
            frequency = self.frequency_change()
        if specification == "":
            specification = input("Enter a task specification:\n")
        not_done = True
        num = 0

        while not_done:

            num += 1
            not_done = self.add_habit_db(num, name, frequency, specification)
        habit = Habit(num, name, frequency,specification, False, 0, [0, 0, 0, 0, 0], 0, datetime.datetime.now().date(),
                      datetime.datetime.now().date(),datetime.datetime.now().date(),[], 0, 0)
        self.habit_list.insert(num - 1, habit)
        print("your habit has been added to your list")
        time.sleep(0.5)

    def add_habit_db(self, num, name, frequency, specification):
        """
        adding the habit to the habit table in the database
        """
        try:
            id = num
            self.cur.execute(
                f"INSERT INTO habits VALUES ({id},{self.id_list[0]},'{name}', {frequency}, '{specification}',0, 0, 00000, 0, datetime('now'), datetime('now'), datetime('now'),'0', 0,0)")
            self.conn.commit()
            return False
        except:
            return True

    def frequency_change(self):
        """returns the number corresponding to the new frequency"""
        x = ""
        while x != "1" or x != "2" or x != "3":
            x = input(
                "what frequency do you want?\n 1. Daily \n 2. Weekly \n 3. monthly \n typ the number you want for your Habit\n")
            if x == "1" or x == "2" or x == "3":
                return int(x)
            else:
                self.wrong_input()

    def wrong_input(self):
        """prints a wrong input message to the user"""
        print("that's not an correct input!")

    def list_habits(self):
        """
        lists all habits from your habit list
        """
        if len(self.habit_list) == 0:
            print("you have no habits")
        else:
            for x in range(0, len(self.habit_list), 1):
                print(f"{x + 1}.", self.habit_list[x].get_name())

    def show_habits(self):
        """
        lets you inspect one habit in more detail
        """
        done = False
        while not done:
            print("Input the number to get more details about the habit")
            self.list_habits()
            x = input(f"{len(self.habit_list) + 1}. back to menu\n")
            try:
                x = int(x)
            except ValueError:
                self.wrong_input()
                time.sleep(0.3)
                continue


            match x:
                case x if 1 <= x <= len(self.habit_list):
                    match self.habit_list[x - 1].get_state():
                        case True:
                            state = "done"
                        case False:
                            state = "still open"

                    match self.habit_list[x - 1].get_frequency():
                        case 1:
                            frequency = "daily"
                        case 2:
                            frequency = "weekly"
                        case 3:
                            frequency = "monthly"
                    dates = []
                    for date in self.habit_list[x-1].get_completion_dates():
                        temp_string = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
                        dates.append(temp_string)
                    print(
                        f"Name: {self.habit_list[x - 1].get_name()}\nstate: " + state + "\nfrequency: " + frequency + f"\nspecification: {self.habit_list[x - 1].get_specification()}\nsteak: {self.habit_list[x - 1].get_streak()}\nhistory: {self.habit_list[x - 1].get_history()}\nlast done: {self.habit_list[x - 1].get_last_done()}\nlongest streak: {self.habit_list[x - 1].get_longest_streak()}\ncreated: {self.habit_list[x - 1].get_created()}\ncompletion dates: {dates}\nfulfilled: {self.habit_list[x - 1].get_fulfilled()}\nfailed: {self.habit_list[x - 1].get_failed()}")
                    done = True

                case x if x == len(self.habit_list) + 1:
                    print("going back to menu")
                    done = True

                case _:
                    self.wrong_input()
                    time.sleep(0.3)
                    continue

    def back_to_menu(self):
        """Holds the user until they press enter"""
        time.sleep(0.3)
        input("press Enter to get back to menu")
        self.menu()

    def complete_habit(self):
        """
        lets you mark one habit as completed
        """
        done = False
        while not done:
            print("Which one did you complete?")
            self.list_habits()
            x = input(f"{len(self.habit_list) + 1}. back to menu\n")
            date = datetime.datetime.today().date()

            try:
                x = int(x)
            except:
                self.wrong_input()
                time.sleep(0.3)
                continue
            match x:
                case x if 1 <= x <= len(self.habit_list):
                    if self.habit_list[x - 1].get_state() != 1:
                        self.habit_list[x - 1].complete_habit(date)
                        print(f"your habit '{self.habit_list[x - 1].get_name()}' is marked as completed\ngood Job!")
                        sleep(0.3)
                        done = True
                    else:
                        print("already done ")
                        sleep(0.3)
                        done = True

                case x if x == len(self.habit_list) + 1:
                    print("going back to menu")
                    time.sleep(0.3)
                    done = True

                case _:
                    self.wrong_input()
                    time.sleep(0.3)
                    continue

    def remove_habit(self):
        """
        gives you the option to remove habits from your list
        """
        done = False
        while not done:
            print("Which one do you want to delete?")
            self.list_habits()
            x = input(f"{len(self.habit_list) + 1}. back to menu\n")

            try:
                x = int(x)
            except:
                self.wrong_input()
                time.sleep(0.3)
                continue

            match x:
                case x if 1 <= x <= len(self.habit_list):
                    self.cur.execute(f"DELETE from habits WHERE habit_id ={self.habit_list[x - 1].get_id()}")
                    self.conn.commit()
                    self.habit_list.remove(self.habit_list[x - 1])
                    for x in range(0, len(self.habit_list), 1):
                        print(self.habit_list[x].get_name())
                    done = True

                case x if x == len(self.habit_list) + 1:
                    print("goning back to menu")
                    time.sleep(0.3)
                    done = True

                case _:
                    self.wrong_input()
                    continue

    def edit_habit(self):
        """Edits ether name, frequency or specification of a habit"""
        done = False
        while not done:
            print("Which one do you want to edit?")
            self.list_habits()
            x = input(f"{len(self.habit_list) + 1}. back to menu\n")

            try:
                x = int(x)

            except:
                self.wrong_input()
                time.sleep(0.3)
                continue

            match x:
                case x if 1 <= x <= len(self.habit_list):
                    y = input("what do you want to edit?\n 1. name\n 2. frequency\n 3. specification\n 4. back\n")
                    match y:
                        case y if y == "1":
                            new_name = input("whats the new name?\n")
                            self.habit_list[x - 1].change_name(new_name)
                            done = True
                        case y if y == "2":
                            new_frequency = self.frequency_change()
                            self.habit_list[x - 1].change_frequency(new_frequency)
                            done = True
                        case y if y == "3":
                            new_spec = input("whats the new specification?\n")
                            self.habit_list[x - 1].change_name(new_spec)
                            done = True
                        case y if y == "4":
                            self.edit_habit()
                            done = True
                        case _:
                            self.wrong_input()
                            continue
                case x if x == len(self.habit_list) + 1:
                    print("going back to menu")
                    time.sleep(0.3)
                    done = True
                case _:
                    continue

    def update_habits(self):
        """
        updates the habit state
        """
        for h in range(0, len(self.habit_list), 1):
            date = datetime.datetime.today().date()
            week = int(datetime.datetime.today().strftime("%V"))
            month = int(datetime.datetime.today().month)
            year = int(datetime.datetime.today().year)
            last_date = self.habit_list[h].get_last_check()
            last_week = datetime.date(last_date.year, last_date.month, last_date.day).strftime("%V")
            last_week = int(last_week)
            last_month = last_date.month
            last_year = last_date.year

            day_dif = date - last_date
            day_dif = int(day_dif.days)

            if year > last_year:
                week_dif = (52 * (year - last_year + 1)) + 52 - last_week + week
                month_dif = (12 * (year - last_year + 1)) + 12 - last_month + month

            else:
                if week > last_week:
                    week_dif = (week - last_week)

                if month > last_month:
                    month_dif = month - last_month

            if date != last_date:
                for y in range(0, day_dif, 1):

                    f = self.habit_list[h].get_frequency()
                    if f == 1:
                        self.habit_list[h].update_habit()

            if week != last_week:
                for z in range(0, week_dif, 1):
                    f = self.habit_list[h].get_frequency()
                    if f == 2:
                        self.habit_list[h].update_habit()

            if month != last_month:
                for a in range(0, month_dif, 1):
                    f = self.habit_list[h].get_frequency()
                    if f == 3:
                        self.habit_list[h].update_habit()
            self.habit_list[h].last_check = date

    def menu(self):
        """
        shows all possible actions and gives you option to choose one
        """
        self.update_habits()
        x = input(
            "What do you want to do?\n 1. Show habits \n 2. complete habit \n 3. analyse habits\n 4. add habit \n 5. edit habit \n 6. remove habit \n 7. close App\n")
        match x:
            case "1":
                self.show_habits()
                self.back_to_menu()
            case "2":
                self.complete_habit()
                self.menu()
            case "3":
                analyse.analyse_menu(self.habit_list)
                self.back_to_menu()
            case "4":
                self.create_habit()
                self.menu()
            case "5":
                self.edit_habit()
                self.menu()
            case "6":
                self.remove_habit()
                self.menu()
            case "7":
                self.save_habits()
                self.cur.close()
                self.conn.close()
                #quit()
            case _:
                self.wrong_input()
                self.menu()

    def login(self, name = "", password = ""):
        """
        login by checking if username and password are correct by comparing with user database
        """
        if name == "":
            name = input("Name:\n")
        if password == "":
            password = input("Password:\n")

        self.cur.execute(f"SELECT password FROM user WHERE name = '{name}'")
        cor_pass = self.cur.fetchone()

        try:
            if password == cor_pass[0]:
                """
                load habits from db when password and username are fitting
                """
                self.cur.execute(f"SELECT user_id FROM user WHERE name = '{name}'")
                id = self.cur.fetchone()
                self.id_list.append(id[0])



            else:
                    print("wrong password")
                    self.login_screen()

        except:
            print("wrong username or password")
            self.login_screen()

        self.load_habits()
        self.menu()

    def load_habits(self):
        """
        loads the habits form the habit table in the database
        """
        data = self.cur.execute(f"SELECT * FROM habits WHERE user_id = {self.id_list[0]}")
        for row in data:
            last_check = datetime.datetime.strptime(row[10], '%Y-%m-%d %H:%M:%S')
            last_check = datetime.datetime(last_check.year, last_check.month, last_check.day).date()
            if row[9] == "never done":
                last_done = last_check
            else:
                last_done = datetime.datetime.strptime(row[9], '%Y-%m-%d')
                last_done = datetime.datetime(last_done.year, last_done.month, last_done.day).date()

            created = datetime.datetime.strptime(row[11], '%Y-%m-%d').date()

            completion_dates = []
            if row[12] != "0":
                temp_string=row[12].split(".")
                for date in temp_string:
                    completion_dates.append(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

            if row[5] == 1:
                state = True
            else:
                state = False

            history = [int(digit) for digit in str(row[7])]
            for y in range(0, 5 - len(history), 1):
                history.insert(0, 0)
            for x in range(0, len(history), 1):
                if history[x] == 1:
                    history.pop(x)
                    history.insert(x, "X")

            habit = Habit(row[0], row[2], row[3],row[4], state, row[6], history, row[8], last_done, last_check, created,completion_dates,row[13],
                          row[14])
            self.habit_list.append(habit)

    def save_habits(self):
        """Saves all the changes to the habits in the database"""

        for x in range(0, len(self.habit_list), 1):
            self.cur.execute(
                f"UPDATE habits SET name= '{self.habit_list[x].get_name()}' WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET frequency= {self.habit_list[x].get_frequency()} WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET specification= '{self.habit_list[x].get_specification()}' WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET state= {self.habit_list[x].get_state()} WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET streak= {self.habit_list[x].get_streak()} WHERE habit_id = {self.habit_list[x].get_id()}")

            for y in range(0, len(self.habit_list[x].get_history()), 1):
                history = self.habit_list[x].get_history()
                if history[y] == "X":
                    history.pop(y)
                    history.insert(y, 1)
            result = int("".join(map(str, history)))
            self.cur.execute(
                f"UPDATE habits SET history= {result} WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET longest_streak= '{self.habit_list[x].get_longest_streak()}' WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET last_done = '{self.habit_list[x].get_last_done()}' WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET last_check = datetime('now') WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET created = '{self.habit_list[x].get_created()}' WHERE habit_id = {self.habit_list[x].get_id()}")
            completion_dates = self.habit_list[x].get_completion_dates()
            if not completion_dates:
                save_string = "0"
            else:
                completion_dates_saves = []
                for date in completion_dates:
                    temp_string = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
                    completion_dates_saves.append(temp_string)
                save_string = '.'.join(completion_dates_saves)
            self.cur.execute(
                f"UPDATE habits SET completion_dates = '{save_string}' WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET fulfilled= {self.habit_list[x].get_fulfilled()} WHERE habit_id = {self.habit_list[x].get_id()}")
            self.cur.execute(
                f"UPDATE habits SET failed= {self.habit_list[x].get_failed()} WHERE habit_id = {self.habit_list[x].get_id()}")

            self.conn.commit()

    def register(self):
        """creates new user with an id and name, password decided by user input"""
        x = input("Whats your name?")
        y = input("What do you want as an password?")
        self.cur.execute("select count(*) from user")
        z = self.cur.fetchone()[0]

        self.cur.execute(f"INSERT INTO user VALUES ({z}, '{x}','{y}')")
        self.conn.commit()
        print(
            f"Your username is '{x}' and your password is '{y}'\ndont forget them you need them everytime you want to login")
        self.login(x, y)

    def login_screen(self):
        """displays the login screen """
        done = False
        while not done:
            x = input("What do you want to do? \n1. Login \n2. Register \n3. Close App\n")
            match x:
                case "1":
                    self.login()
                    done = True
                case "2":
                    self.register()
                    done = True
                case "3":
                    quit()

                case _:
                    self.wrong_input()
