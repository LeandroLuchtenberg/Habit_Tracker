class Habit():
    """Class representing a habit with properties like name, frequency,state and an id."""
    def __init__(self, id, name, frequency,specification,state, streak, history, longest_streak, last_done, last_check, created,completion_dates, fulfilled, failed):
        self.id = id
        self.name = name
        self.frequency = frequency
        self.specification = specification
        self.state = state
        self.streak = streak
        self.history = history
        self.longest_streak = longest_streak
        self.last_done = last_done
        self.last_check = last_check
        self.created = created
        self.completion_dates = completion_dates
        self.fulfilled = fulfilled
        self.failed = failed


    """get functions of habit class"""

    def get_id(self):
        return self.id

    def get_specification(self):
        return self.specification

    def get_state(self):
        return self.state

    def get_name(self):
        return self.name

    def get_streak(self):
        return self.streak

    def get_history(self):
        return self.history

    def get_frequency(self):
        return self.frequency

    def get_longest_streak(self):
        return self.longest_streak

    def get_last_done(self):
        if self.fulfilled == 0:
            return "never done"
        else:
            return self.last_done

    def get_last_check(self):
        return self.last_check

    def get_created(self):
        return self.created

    def get_completion_dates(self):
        return self.completion_dates

    def get_failed(self):
        return self.failed

    def get_fulfilled(self):
        return self.fulfilled


    """functions to automatically change properties of habit objects"""

    def complete_habit(self, date):
        """Markes habit as completed, calls to update the streak and saves the date """
        self.state = True
        self.add_streak()
        self.update_history(True)
        self.fulfilled += 1
        self.last_done = date
        self.completion_dates.append(date)

    def update_habit(self):
        """resets the habit after a period ended"""
        if self.state:
            self.state = False
        else:
            self.update_history(False)
            self.failed +=1
            self.streak = 0

    def add_streak(self):
        """adds 1 to the streak and checks for new longest streak"""
        self.streak += 1
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak

    def update_history(self, done):
        """updates the history of the habit given if it was fulfilled or not """
        self.history.pop(0)
        if done == True:
            self.history.append("X")
        else:
            self.history.append(0)

    """functions to change properties of habit objects through user input"""
    def change_name(self, name):
        self.name = name

    def change_spec(self, spec):
        self.specification = spec

    def change_frequency(self, frequency):
        self.frequency = frequency

