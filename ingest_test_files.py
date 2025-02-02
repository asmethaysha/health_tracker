import os
import sys
import sqlite3
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


def insert_query_populator(insert_query_format, file, test_dir):
    """
    Populates the actual full insert query using the format passed in
    """
    full_path = os.path.join(test_dir, file)
    f = open(full_path, "r")
    data = f.read()
    f.close()
    if not len(data.strip()):
        return
    data = data.split("\n")[1:]  # excluding header
    data = [x for x in data if x.strip()]
    for datum in data:
        # datum is comma separated values
        string_datum = datum.split(",")
        string_datum = ["'" + x + "'" for x in string_datum]
        string_datum = ",".join(string_datum)
        insert_query_format += "( {} ),\n".format(string_datum)
    insert_query_format = insert_query_format.strip()[:-1] + ";"
    # print(insert_query_format)
    return insert_query_format


def main():
    curr_dir = pathlib.Path().resolve()
    test_dir, test_db_path = os.path.join(curr_dir, "test_files"), os.path.join(
        curr_dir, "test.db"
    )
    if not os.listdir(test_dir):
        print("No files found here, exiting!")
        return
    if not os.path.exists(test_db_path):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        # create db if DNE
        # Create tables that don't exist
        create_all_tables = (
            "CREATE TABLE SLEEP_TRACKING(starting_timestamp TIMESTAMP NOT NULL, ending_timestamp TIMESTAMP NOT NULL, time_slept INTEGER NOT NULL, comments VARCHAR); "
            "CREATE TABLE HISTORICAL_WEIGHT(timestamp TIMESTAMP NOT NULL, weight FLOAT NOT NULL); "
            "CREATE TABLE FOOD_TRACKING(timestamp TIMESTAMP NOT NULL, meal_category VARCHAR NOT NULL, food_name VARCHAR NOT NULL, num_servings FLOAT NOT NULL, mass FLOAT, vitA FLOAT, vitC FLOAT, vitD FLOAT, vitE FLOAT, iron FLOAT, sodium FLOAT, carbohydrates FLOAT, comments VARCHAR); "
            "CREATE TABLE MOOD_TRACKING(timestamp TIMESTAMP, happiness_rating INTEGER, comments VARCHAR); "
            "CREATE TABLE EXERCISE_TRACKING(starting_timestamp TIMESTAMP NOT NULL, ending_timestamp TIMESTAMP NOT NULL, exercise_name VARCHAR NOT NULL, calories INTEGER NOT NULL, reps INTEGER, steps INTEGER, comments VARCHAR);"
        )
        create_all_tables = create_all_tables.split(";")
        create_all_tables = [x.strip() for x in create_all_tables]
        for query in create_all_tables:
            cursor.execute(query)
        conn.commit()
        conn.close()
    if os.path.exists(test_db_path):
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        check_query = "SELECT * FROM sqlite_schema WHERE type='table' ORDER BY name"
        cursor.execute(check_query)
        all_table_data = cursor.fetchall()
        all_table_names = [x[1] for x in all_table_data]
        for table in all_table_data:
            # this is where we create insert commands that we will use for actual ingestion steps
            file_substr = table[1].lower()
            files_to_parse = os.listdir(test_dir)
            files_to_parse = [file for file in files_to_parse if file_substr in file]
            create_cmd = table[4]
            insert_query_format = convert_to_insert_template(create_cmd)
            for file in files_to_parse:
                insert_query = insert_query_populator(
                    insert_query_format, file, test_dir
                )
                if insert_query:
                    cursor.execute(insert_query)
    conn.commit()
    conn.close()


main()
