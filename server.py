from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database with EXERCISE_TRACKING table
def init_db():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()

#exercise table
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

#weight and body fat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HISTORICAL_WEIGHT (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            weight FLOAT,
            body_fat_percentage FLOAT
        )
    ''')


# sleep table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SLEEP_TRACKING (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            starting_timestamp TIMESTAMP,
            ending_timestamp TIMESTAMP,
            time_slept FLOAT,
            comments VARCHAR
        )
    ''')

# mood table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MOOD_TRACKING (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            happiness INTEGER,
            comments VARCHAR
        )
    ''')


#meal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MEAL_TRACKING (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_category VARCHAR,
            calories FLOAT,
            number_of_servings FLOAT,
            weight_grams FLOAT,
            vitamins FLOAT,
            minerals FLOAT,
            carbohydrates FLOAT,
            protein FLOAT,
            comments VARCHAR,
            timestamp TIMESTAMP
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

        conn = sqlite3.connect("healthfit.db")
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
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT starting_timestamp, ending_timestamp, exercise_name, calories_burned, repetitions, steps, comments FROM EXERCISE_TRACKING ORDER BY starting_timestamp DESC")
    workouts = cursor.fetchall()
    conn.close()

    return render_template('view_workouts.html', workouts=workouts)

@app.route('/calories_chart')
def calories_chart():
    conn = sqlite3.connect("healthfit.db")
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


#Weight logs
@app.route('/log_weight', methods=['GET', 'POST'])
def log_weight():
    if request.method == 'POST':
        timestamp = request.form.get('timestamp')
        weight = request.form.get('weight')
        body_fat_percentage = request.form.get('body_fat_percentage')

        conn = sqlite3.connect("healthfit.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO HISTORICAL_WEIGHT (timestamp, weight, body_fat_percentage)
            VALUES (?, ?, ?)
        ''', (timestamp, weight, body_fat_percentage))
        conn.commit()
        conn.close()

        return redirect(url_for('view_weight'))
    return render_template('log_weight.html')


@app.route('/weight_history')
def view_weight():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, weight, body_fat_percentage FROM HISTORICAL_WEIGHT ORDER BY timestamp DESC")
    weight_history = cursor.fetchall()
    conn.close()

    return render_template('view_weight.html', weight_history=weight_history)


@app.route('/weight_chart')
def weight_chart():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, weight FROM HISTORICAL_WEIGHT ORDER BY timestamp ASC")
    data = cursor.fetchall()
    conn.close()

    weight_data = {
        "labels": [row[0] for row in data],
        "values": [row[1] for row in data]
    }
    return jsonify(weight_data)


@app.route('/view_weight_chart')
def view_weight_chart():
    return render_template('weight_chart.html')


#Happiness Logs
@app.route('/log_happiness', methods=['GET', 'POST'])
def log_happiness():
    if request.method == 'POST':
        timestamp = request.form.get('timestamp')
        happiness = request.form.get('happiness')
        comments = request.form.get('comments')

        conn = sqlite3.connect("healthfit.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MOOD_TRACKING (timestamp, happiness, comments)
            VALUES (?, ?, ?)
        ''', (timestamp, happiness, comments))
        conn.commit()
        conn.close()

        return redirect(url_for('view_happiness'))

    return render_template('log_happiness.html')



@app.route('/happiness_index')
def view_happiness():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, happiness, comments FROM MOOD_TRACKING ORDER BY timestamp DESC")
    happiness_index = cursor.fetchall()
    conn.close()

    return render_template('view_happiness.html', happiness_index=happiness_index)



@app.route('/happiness_chart')
def happiness_chart():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, happiness FROM MOOD_TRACKING ORDER BY timestamp ASC")
    data = cursor.fetchall()
    conn.close()

    happiness_data = {
        "labels": [row[0] for row in data],  
        "values": [row[1] for row in data]   
    }

    return jsonify(happiness_data)

@app.route('/view_happiness_chart')
def view_happiness_chart():
    return render_template('happiness_chart.html')


# Log Nutrition
@app.route('/log_meal', methods=['GET', 'POST'])
def log_meal():
    if request.method == 'POST':
        
        meal_category = request.form.get('meal_category')
        calories = request.form.get('calories')
        number_of_servings = request.form.get('number_of_servings')
        weight_grams = request.form.get('weight_grams')
        vitamins = request.form.get('vitamins')
        minerals = request.form.get('minerals')
        carbohydrates = request.form.get('carbohydrates')
        protein = request.form.get('protein')
        comments = request.form.get('comments')
        timestamp = request.form.get('timestamp')

        conn = sqlite3.connect("healthfit.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MEAL_TRACKING (meal_category, calories, number_of_servings, weight_grams, vitamins, minerals, carbohydrates, protein, comments, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (meal_category, calories, number_of_servings, weight_grams, vitamins, minerals, carbohydrates, protein, comments, timestamp))
        conn.commit()
        conn.close()

        return redirect(url_for('view_meals'))

    return render_template('log_meal.html')


@app.route('/meals')
def view_meals():
    conn = sqlite3.connect("healthfit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT meal_category, calories, number_of_servings, weight_grams, vitamins, minerals, carbohydrates, protein, comments, timestamp FROM MEAL_TRACKING ORDER BY timestamp DESC")
    meals = cursor.fetchall()
    conn.close()

    return render_template('view_meals.html', meals=meals)



# Home Page
@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
