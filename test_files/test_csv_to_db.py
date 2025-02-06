import os
import pytest
import sqlite3
import pandas as pd
import pathlib
import datetime
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
# proj_dir = pathlib.Path(pathlib.Path(current_file)
test_db_path = os.path.join(proj_dir, "test.db")
test_files_path = pathlib.Path(__file__).resolve().parent
conn = sqlite3.connect(test_db_path)


def test_db_exists():
    assert os.path.exists(test_db_path)


def test_exercise_tracking_has_content():
    path = os.path.join(proj_dir, "test_files")
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
    start, end = start.strftime("%Y%m%d %H%M%S"), end.strftime("%Y%m%d %H%M%S")
    exercise_name = "Running"
    calories, reps, steps = "800", "", "10000"
    comments = "My first 10k!"
    insert_query = "INSERT INTO EXERCISE_TRACKING (starting_timestamp,ending_timestamp,exercise_name,calories,reps,steps,comments)"
    insert_query += f"VALUES ('{start}','{end}','{exercise_name}','{calories}','{reps}','{steps}','{comments}');"
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
    path = os.path.join(proj_dir, "test_files")
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


def test_historical_weight_has_content():
    path = os.path.join(proj_dir, "test_files")
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
    start = start.strftime("%Y%m%d %H%M%S")
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
    path = os.path.join(proj_dir, "test_files")
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
