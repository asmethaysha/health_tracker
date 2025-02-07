import sqlite3

conn = sqlite3.connect("healthfit.db")
cursor = conn.cursor()

# Create SLEEP_TRACKING table without NULL constraints
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SLEEP_TRACKING (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        starting_timestamp TIMESTAMP,
        ending_timestamp TIMESTAMP,
        time_slept FLOAT,
        comments VARCHAR
    )
''')

# Initialize the database with EXERCISE_TRACKING table
cursor.execute('''
        CREATE TABLE IF NOT EXISTS EXERCISE_TRACKING (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            starting_timestamp TIMESTAMP,
            ending_timestamp TIMESTAMP,
            exercise_name VARCHAR,
            calories_burned INTEGER,
            repetitions INTEGER,
            steps INTEGER,
            comments VARCHAR
        )
    ''')
    


conn.commit()
conn.close()
print("SLEEP_TRACKING table created successfully!")
