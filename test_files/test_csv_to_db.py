import os
import pytest
import sqlite3
import pandas as pd
import pathlib
import pickle
import datetime
import matplotlib.pyplot as plt
from datetime import timedelta


def convert_to_insert_template(create_cmd):
    # converts the create command used by a table to a formattable insert query.
    # General structure of input: CREATE TABLE EXERCISE_TRACKING(starting_ts TIMESTAMP NOT NULL, ending_ts TIMESTAMP NOT NULL, exercise_name VARCHAR NOT NULL, calories INTEGER NOT NULL, reps INTEGER, steps INTEGER, comments VARCHAR)
    # General structure of output:
    # INSERT INTO table1 (column1,column2 ,..)
    # VALUES
    #    (value1,value2 ,... valueN),
    #    (value1,value2 ,...),
    #     ...
    #    (value1,value2 ,...);
    insert_query = ""
    # part1
    table = create_cmd.split("(")[0].split()[-1]
    insert_query += f"INSERT INTO {table} "
    columns = create_cmd.split("(")[1]
    columns = columns.replace(" NOT NULL", "").replace(")", "").split(",")
    columns = [c.split()[0] for c in columns]
    # part2
    insert_query += "("
    for c in columns:
        insert_query += f"{c}, "
    insert_query = insert_query[:-2]  # get rid of last comma and space
    insert_query += ")\n"
    # part3
    insert_query += "VALUES\n"
    # insert_query += " ( {} )"  # comma separated values go here, commented on purpose
    return insert_query


proj_dir = pathlib.Path().resolve()
test_db_path = os.path.join(proj_dir, "test.db")
test_files_path = pathlib.Path(__file__).resolve().parent
conn = sqlite3.connect(test_db_path)


def test_db_exists():
    assert os.path.exists(test_db_path)


def test_exercise_tracking_has_content():
    query = "SELECT * FROM EXERCISE_TRACKING"
    df_test_db = pd.read_sql_query(query, conn)
    df_test_db.fillna("", inplace=True)
    test_files = [x for x in os.listdir(test_files_path) if "exercise_tracking" in x]
    for file in test_files:
        file_path = os.path.join(test_files_path, file)
        df_csv = pd.read_csv(file_path)
        assert list(df_csv.columns) == list(df_test_db.columns)
        df_csv.fillna("", inplace=True)
        merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
        missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )
        # Test fails if there are missing rows
        assert (
            missing_rows.empty
        ), f"Missing rows in database:\n{missing_rows.to_string()}"


def test_insert_delete_exercise_tracking():
    cursor = conn.cursor()
    select_query = "SELECT count(*) FROM EXERCISE_TRACKING"
    cursor.execute(select_query)
    old_count = int(cursor.fetchall()[0][0])
    assert old_count is not None
    start = datetime.datetime.now()
    end = start + timedelta(minutes=60)
    start, end = start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")
    exercise_name = "Running"
    calories_burned, reps, steps = "800", "", "10000"
    comments = "My first 10k!"
    insert_query = "INSERT INTO EXERCISE_TRACKING (starting_timestamp,ending_timestamp,exercise_name,calories_burned,reps,steps,comments)"
    insert_query += f"VALUES ('{start}','{end}','{exercise_name}','{calories_burned}','{reps}','{steps}','{comments}');"
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count - old_count == 1
    del_query = f"DELETE FROM EXERCISE_TRACKING WHERE comments='{comments}'"
    print(del_query)
    cursor.execute(del_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count == old_count


def test_food_tracking_has_content():
    query = "SELECT * FROM FOOD_TRACKING"
    df_test_db = pd.read_sql_query(query, conn)
    df_test_db.fillna("", inplace=True)
    test_files = [x for x in os.listdir(test_files_path) if "food_tracking" in x]
    for file in test_files:
        file_path = os.path.join(test_files_path, file)
        df_csv = pd.read_csv(file_path)
        assert list(df_csv.columns) == list(df_test_db.columns)
        df_csv.fillna("", inplace=True)
        merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
        missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )
        # Test fails if there are missing rows
        assert (
            missing_rows.empty
        ), f"Missing rows in database:\n{missing_rows.to_string()}"


def test_insert_delete_food_tracking():
    cursor = conn.cursor()
    select_query = "SELECT count(*) FROM FOOD_TRACKING"
    cursor.execute(select_query)
    old_count = int(cursor.fetchall()[0][0])
    assert old_count is not None
    timestamp = datetime.datetime.now()
    meal_category, food_name, comments = (
        "midnight_snack",
        "popcorn",
        "Should not have eaten this",
    )
    calories, num_servings, mass = 400, 2, 250
    vitaminA, vitaminC, vitaminD, vitaminE = 0, 0, 0, 0
    iron, sodium, carbohydrates = 1, 1000, 100
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    insert_query = "INSERT INTO FOOD_TRACKING (timestamp,meal_category,calories,food_name,num_servings,mass,vitaminA,vitaminC,vitaminD,vitaminE,iron,sodium,carbohydrates,comments)"
    insert_query += f"VALUES ('{timestamp}','{meal_category}','{calories}','{food_name}','{num_servings}','{mass}','{vitaminA}','{vitaminC}','{vitaminD}','{vitaminE}','{iron}','{sodium}','{carbohydrates}','{comments}');"
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count - old_count == 1
    del_query = f"DELETE FROM FOOD_TRACKING WHERE comments='{comments}'"
    cursor.execute(del_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count == old_count


def test_historical_weight_has_content():
    query = "SELECT * FROM HISTORICAL_WEIGHT"
    df_test_db = pd.read_sql_query(query, conn)
    df_test_db.fillna("", inplace=True)
    test_files = [x for x in os.listdir(test_files_path) if "historical_weight" in x]
    for file in test_files:
        file_path = os.path.join(test_files_path, file)
        df_csv = pd.read_csv(file_path)
        assert list(df_csv.columns) == list(df_test_db.columns)
        df_csv.fillna("", inplace=True)
        merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
        missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )
        # Test fails if there are missing rows
        assert (
            missing_rows.empty
        ), f"Missing rows in database:\n{missing_rows.to_string()}"


def test_insert_delete_historical_weight():
    cursor = conn.cursor()
    select_query = "SELECT count(*) FROM HISTORICAL_WEIGHT"
    cursor.execute(select_query)
    old_count = int(cursor.fetchall()[0][0])
    assert old_count is not None
    start = datetime.datetime.now()
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    weight = "60"
    insert_query = "INSERT INTO HISTORICAL_WEIGHT (timestamp,weight)"
    insert_query += f"VALUES ('{start}','{weight}');"
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count - old_count == 1
    del_query = f"DELETE FROM HISTORICAL_WEIGHT WHERE timestamp='{start}' and weight='{weight}';"
    print(del_query)
    cursor.execute(del_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count == old_count


def test_sleep_tracking_has_content():
    query = "SELECT * FROM SLEEP_TRACKING"
    df_test_db = pd.read_sql_query(query, conn)
    df_test_db.fillna("", inplace=True)
    test_files = [x for x in os.listdir(test_files_path) if "sleep_tracking" in x]
    for file in test_files:
        file_path = os.path.join(test_files_path, file)
        df_csv = pd.read_csv(file_path)
        assert list(df_csv.columns) == list(df_test_db.columns)
        df_csv.fillna("", inplace=True)
        merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
        missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )
        # Test fails if there are missing rows
        assert (
            missing_rows.empty
        ), f"Missing rows in database:\n{missing_rows.to_string()}"


def test_insert_delete_sleep_tracking():
    cursor = conn.cursor()
    select_query = "SELECT count(*) FROM SLEEP_TRACKING"
    cursor.execute(select_query)
    old_count = int(cursor.fetchall()[0][0])
    assert old_count is not None
    start = datetime.datetime.now()
    end = start + timedelta(hours=6)
    time_slept = (end - start).total_seconds()
    start, end = start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")
    comments = "Goodnight"
    weight = "60"
    insert_query = "INSERT INTO SLEEP_TRACKING (starting_timestamp,ending_timestamp,time_slept,comments)"
    insert_query += f"VALUES ('{start}','{end}','{time_slept}','{comments}');"
    cursor.execute(insert_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count - old_count == 1
    del_query = f"DELETE FROM SLEEP_TRACKING WHERE starting_timestamp='{start}' and time_slept='{time_slept}';"
    cursor.execute(del_query)
    conn.commit()
    cursor.execute(select_query)
    new_count = int(cursor.fetchall()[0][0])
    assert new_count is not None
    assert new_count == old_count


def test_successful_generation_display_of_plots():
    all_tables_dict = {
        "HISTORICAL_WEIGHT": ["weight", "bmi"],
        "SLEEP_TRACKING": ["time_slept"],
        "FOOD_TRACKING": [
            "calories",
            "mass",
            "vitaminA",
            "vitaminC",
            "vitaminD",
            "vitaminE",
            "iron",
            "sodium",
            "carbohydrates",
        ],
        "MOOD_TRACKING": ["happiness_rating"],
        "EXERCISE_TRACKING": [
            "steps",
            "calories_burned",
            "exercise_time",
        ],
    }

    def plot_fn():
        plt.show()
        return True

    for table in all_tables_dict.keys():
        for y_axis in all_tables_dict[table]:
            img_name = f"{table}_{y_axis}.jpg"
            pkl_name = f"{table}_{y_axis}.pkl"
            img_file_path = os.path.join(test_files_path, img_name)
            pkl_file_path = os.path.join(test_files_path, pkl_name)
            assert os.path.exists(img_file_path)
            with open(pkl_file_path, "rb") as f:
                fig = pickle.load(f)
                assert fig
                with plt.ion():
                    assert plot_fn()
