import sqlite3

def get_db(name="habits.db"):
    db = sqlite3.connect(name)
    return db

def create_table(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS
    user(user_id INTEGER PRIMARY KEY, name TEXT, password TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS
    habits(habit_id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency INTEGER, state INTEGER, streak INTEGER, history INTEGER, longest_streak INTEGER,date TEXT, fullfilled INTEGER, failed INTEGER, FOREIGN KEY(user_id) REFERENCES user(user_id))""")
    db.commit()

def add_habit(db, id, user_id, name, frequency):
    cur = db.cursor()
    cur.execute(f"INSERT INTO habits VALUES ({id},{user_id},'{name}', {frequency}, 0, 0, 00000, 0, datetime('now'), 0,0)")
    db.commit()

def del_habit(db, id):
    cur = db.cursor()
    cur.execute(f"DELETE from habits WHERE habit_id ={id}")
    db.commit()

def get_password():
    a = 1
