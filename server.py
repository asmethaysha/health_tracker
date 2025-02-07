from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database with EXERCISE_TRACKING table
def init_db():
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()
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

init_db()

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        starting_timestamp = request.form.get('starting_timestamp')
        ending_timestamp = request.form.get('ending_timestamp')
        exercise_name = request.form.get('exercise_name')
        calories_burned = request.form.get('calories_burned')
        repetitions = request.form.get('repetitions')
        steps = request.form.get('steps')
        comments = request.form.get('comments')

        conn = sqlite3.connect("workouts.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO EXERCISE_TRACKING (starting_timestamp, ending_timestamp, exercise_name, calories_burned, repetitions, steps, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (starting_timestamp, ending_timestamp, exercise_name, calories_burned, repetitions, steps, comments))
        conn.commit()
        conn.close()

        return redirect(url_for('view_workouts'))

    return render_template('log_workout.html')

@app.route('/workouts')
def view_workouts():
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT starting_timestamp, ending_timestamp, exercise_name, calories_burned, repetitions, steps, comments FROM EXERCISE_TRACKING ORDER BY starting_timestamp DESC")
    workouts = cursor.fetchall()
    conn.close()

    return render_template('view_workouts.html', workouts=workouts)

@app.route('/calories_chart')
def calories_chart():
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT starting_timestamp, calories_burned FROM EXERCISE_TRACKING ORDER BY starting_timestamp ASC")
    data = cursor.fetchall()
    conn.close()

    chart_data = {
        "labels": [row[0] for row in data],  
        "values": [row[1] for row in data]   
    }

    return jsonify(chart_data)

@app.route('/view_chart')
def view_chart():
    return render_template('calories_chart.html')




# Log Sleep Route
@app.route('/log_sleep', methods=['POST'])
def log_sleep():
    sleep_start = request.form.get('sleep_start')
    sleep_end = request.form.get('sleep_end')

    # Calculate time slept
    start_time = datetime.strptime(sleep_start, "%Y-%m-%dT%H:%M")
    end_time = datetime.strptime(sleep_end, "%Y-%m-%dT%H:%M")
    time_slept = round((end_time - start_time).total_seconds() / 3600, 2)  # Convert to hours

    data = (sleep_start, sleep_end, time_slept, request.form.get('sleep_comments') or None)

    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO SLEEP_TRACKING (starting_timestamp, ending_timestamp, time_slept, comments)
        VALUES (?, ?, ?, ?)
    ''', data)

    conn.commit()
    conn.close()

    return redirect('/sleep')


# Display Logged Sleep Data
@app.route('/sleep')
def view_sleep():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SLEEP_TRACKING ORDER BY starting_timestamp DESC")
    sleep_data = cursor.fetchall()
    conn.close()

    return render_template("sleep.html", sleep_data=sleep_data)


# Route to fetch sleep data as JSON for the chart
@app.route('/get_sleep_data')
def get_sleep_data():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT starting_timestamp, time_slept FROM SLEEP_TRACKING ORDER BY starting_timestamp ASC")
    data = cursor.fetchall()
    conn.close()

    sleep_data = {"labels": [row[0] for row in data], "values": [row[1] for row in data]}
    return jsonify(sleep_data)

@app.route('/sleep_chart')
def sleep_chart():
    return render_template('sleep_chart.html')

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
