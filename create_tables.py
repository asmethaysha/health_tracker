import sqlite3

def init_db():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(HISTORICAL_WEIGHT)")
    table_info = cursor.fetchall()

    if table_info:
        print("Table HISTORICAL_WEIGHT exists.")
    else:
        print("Table HISTORICAL_WEIGHT does not exist.")
    
    conn.commit()
    conn.close()


"""
    
    

    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SLEEP_TRACKING (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        starting_timestamp TIMESTAMP,
        ending_timestamp TIMESTAMP,
        time_slept FLOAT,
        comments VARCHAR
    )
''')

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

    """

    

   

    




init_db()
print("done")

