import unittest
from unittest.mock import patch
from habit_tracker import Habit_Tracker
from datetime import datetime
import datetime
import analyse




class Testhabittracker(unittest.TestCase):

    def setUp(self):
        """Sets up a test environment"""
        self.tracker = Habit_Tracker("HabitTrackerTest.db")
        self.tracker.cur.execute("DELETE FROM habits")
        self.tracker.cur.execute("DELETE FROM user")
        name = "Test"
        password = "theFirst"
        date = datetime.datetime.now().date()
        self.tracker.cur.execute(f"INSERT INTO user VALUES (0, '{name}','{password}')")
        self.tracker.cur.execute(f"INSERT INTO habits VALUES (0,0,'walking', 1, '10k steps',0, 0, 00000, 0, 'never done', datetime('now'),'2025-04-28','0', 0,0)")
        self.tracker.id_list.append(0)

    def test1_register(self):
        """test the register function"""
        print("Test1 register")
        name = "register"
        password = "theFirst"

        self.tracker.cur.execute("select count(*) from user")
        z = self.tracker.cur.fetchone()[0]

        self.tracker.cur.execute(f"INSERT INTO user VALUES ({z}, '{name}','{password}')")
        self.tracker.conn.commit()

        print(
            f"Your username is '{name}' and your password is '{password}'\ndont forget them you need them everytime you want to login")
        self.tracker.cur.execute(f"select * from user WHERE user_id = {z}")
        test = self.tracker.cur.fetchone()
        self.assertEqual(test[1], name)
        self.assertEqual(test[2], password)

    def test2_LoginAndLoading(self):
        print("Test2 Log in and Loading")

        name = "Test"
        password = "theFirst"


        self.tracker.conn.commit()

        self.tracker.cur.execute(f"SELECT password FROM user WHERE name = '{name}'")
        cor_pass = self.tracker.cur.fetchone()

        # try:
        if password == cor_pass[0]:
            """
            load habits from db when password and username are fitting
            """
            self.tracker.cur.execute(f"SELECT user_id FROM user WHERE name = '{name}'")
            id = self.tracker.cur.fetchone()
            self.tracker.id_list.append(id[0])

            self.tracker.load_habits()
        else:
            print("wrong password")
            self.tracker.login()


        self.assertEqual(self.tracker.habit_list[0].get_name(), "walking")
        print("login and loading of habits confirmed ")


    def test3_create_habit(self):
        """Tests to create a new habit"""
        print("Test3 creation of habit")

        name = "drinking"
        frequency = 1
        specification = "2 Liters"
        self.tracker.create_habit(name, frequency, specification)


        self.assertEqual(self.tracker.habit_list[0].get_name(), name)
        self.assertEqual(self.tracker.habit_list[0].get_frequency(), frequency)
        print("creation of habit was successful")

    @patch('builtins.input', return_value="1")
    def test4_show_habit(self, mock_input):
        print("Test4 show habit")
        """"
        Setting up habits to take a look at
        """
        name = ["working", "drinking", "jogging"]
        frequency = [1, 2, 3]

        for x in range(len(name)):
            self.tracker.create_habit(name[x], frequency[x])

        """
        listing all habits and taking a closer look at the first one 
        """
        self.tracker.show_habits()
        print("functions to show all habits and details about certain ones is working")

    @patch('builtins.input', side_effect=['1', "1", "reading"])# 1, 1 is the way to navigate to edit the name of the habit and reading is the new name
    def test5_edit_habit(self, mock_input):
        """Test the edit habit function """
        print("Test5 edit habit")
        name = "working"
        frequency = 1
        specification = "It"
        self.tracker.create_habit(name, frequency, specification)

        self.tracker.edit_habit()

        self.assertEqual(self.tracker.habit_list[0].get_name(), "reading") # check if it worked replacing the name

    def test6_complete_habits(self):
        print("Test6 edit habit and streak function")
        name = "working"
        frequency = 1
        specification ="It"
        self.tracker.create_habit(name, frequency, specification)

        self.tracker.habit_list[0].complete_habit(datetime.datetime.now().date())

        self.assertEqual(self.tracker.habit_list[0].get_state(), 1)
        self.assertEqual(self.tracker.habit_list[0].get_streak(), 1)
        print("habit is marked as completed and streak got updated successfully")

    @patch('builtins.input', return_value="2")
    def test7_analytics(self, mock_input):
        """tests the analytics menu"""
        print("Test7 anaöytics module")
        name = ["working", "drinking", "jogging"]
        frequency = [1, 2, 2]

        for x in range(len(name)):
            self.tracker.create_habit(name[x], frequency[x])

        analyse.show_streaks(self.tracker.get_habit_list())
        analyse.show_longest_streaks(self.tracker.get_habit_list())
        analyse.show_habits_by_periodicity(self.tracker.get_habit_list())
        print("all analysing tools are working")



if __name__ == '__main__':
    unittest.main()  # Run the test suite
