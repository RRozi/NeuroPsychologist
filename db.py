import sqlite3

connect = sqlite3.connect("database.db", check_same_thread=False)
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    history TEXT,
                    feedback TEXT)''')