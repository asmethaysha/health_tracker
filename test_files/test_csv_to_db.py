import os
import sys
import numpy as np
import pytest
import sqlite3
import pandas as pd
import pathlib


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

# @pytest.fixture
# def db_connection():
#     """Creates a connection to the SQLite database."""
#     conn = sqlite3.connect(test_db_path)
#     yield conn
#     conn.close()


print(test_files_path)

# @pytest.fixture
# def cursor():
# yield conn().cursor()


def test_db_exists():
    assert os.path.exists(test_db_path)


def test_exercise_tracking_has_content():
    path = os.path.join(proj_dir, "test_files")
    query = "SELECT * FROM EXERCISE_TRACKING"
    df_test_db = pd.read_sql_query(query, conn)
    df_test_db.fillna("", inplace=True)
    exercise_files = [
        x for x in os.listdir(test_files_path) if "exercise_tracking" in x
    ]
    for file in exercise_files:
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


# def test_food_tracking_has_content():
#     try:
#         path = os.path.join(proj_dir, "test_files")
#         query = "SELECT * FROM FOOD_TRACKING"
#         df_test_db = pd.read_sql_query(query, conn)
#         for file in os.listdir():
#             df_csv = pd.read_csv(file)
#             assert df_csv.columns == df_test_db.columns
#             merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
#             missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
#                 columns=["_merge"]
#             )
#             assert (
#                 missing_rows.empty
#             )  # there are no rows that exist in csv but not in db
#     except:
#         print(" 4")


# def test_historical_weight_has_content():
#     try:
#         path = os.path.join(proj_dir, "test_files")
#         query = "SELECT * FROM HISTORICAL_WEIGHT"
#         df_test_db = pd.read_sql_query(query, conn)
#         for file in os.listdir():
#             df_csv = pd.read_csv(file)
#             assert df_csv.columns == df_test_db.columns
#             merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
#             missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
#                 columns=["_merge"]
#             )
#             assert (
#                 missing_rows.empty
#             )  # there are no rows that exist in csv but not in db
#     except:
#         print(" 5")


# def test_mood_tracking_has_content():
#     try:
#         path = os.path.join(proj_dir, "test_files")
#         query = "SELECT * FROM MOOD_TRACKING"
#         df_test_db = pd.read_sql_query(query, conn)
#         for file in os.listdir():
#             df_csv = pd.read_csv(file)
#             assert df_csv.columns == df_test_db.columns
#             merged_data = df_csv.merge(df_test_db, how="left", indicator=True)
#             missing_rows = merged_data[merged_data["_merge"] == "left_only"].drop(
#                 columns=["_merge"]
#             )
#             assert (
#                 missing_rows.empty
#             )  # there are no rows that exist in csv but not in db
#     except:
#         print(" 6")
