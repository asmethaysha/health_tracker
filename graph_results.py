import os
import sys
import pickle
import pandas as pd
import pathlib
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random

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


height = random.uniform(1.4, 3.0)


def bmi_calculator(df):
    df["bmi"] = df["weight"] / (height * height)
    return df


def time_slept_to_hrs(df):
    df["time_slept_seconds"] = df["time_slept"]
    df["time_slept"] = df["time_slept"] / 3600
    return df


def exercise_time(df):
    df["exercise_time"] = pd.to_datetime(df["ending_timestamp"]) - pd.to_datetime(
        df["starting_timestamp"]
    )
    df["exercise_time"] = df["exercise_time"].dt.total_seconds() / 60
    return df


all_functions_dict = {
    "bmi": bmi_calculator,
    "time_slept": time_slept_to_hrs,
    "exercise_time": exercise_time,
}

conn = sqlite3.connect("test.db")


def main():
    proj_dir = pathlib.Path().resolve()
    test_files_path = os.path.join(proj_dir, "test_files")
    for table in all_tables_dict.keys():
        x_axis = ""
        for try_x_axis in ["timestamp", "starting_timestamp"]:
            query = f"SELECT * FROM {table} order by {try_x_axis}"
            try:
                df = pd.read_sql_query(query, conn)
                x_axis = try_x_axis
            except:
                continue
        if not x_axis:
            print("ERROR - NO VALID COLUMN FOUND")
            print(table)
            sys.exit(1)
        for y_axis in all_tables_dict[table]:
            if y_axis in all_functions_dict:
                update_df = all_functions_dict[y_axis]
                df = update_df(df)
            df[x_axis] = pd.to_datetime(df[x_axis], format="%Y-%m-%d %H:%M:%S")
            plt.figure(figsize=(10, 5))
            try:
                plt.plot(df[x_axis], df[y_axis], marker="o", linestyle="-")
            except Exception as e:
                print(e)
                print("TABLE failed", table, y_axis)
            plt.xlabel("Date & Time")
            title = y_axis
            if title == "bmi":
                title = "BMI"
            else:
                if "vit".lower() in title.lower():
                    title = title[:-1].capitalize() + " " + y_axis[-1]
                if "_" in title:
                    title = " ".join([x.capitalize() for x in title.split("_")])
                else:
                    title = title.capitalize()
            plt.ylabel(y_axis.replace("_", " "))
            plt.title(f"{title} Graph")
            plt.xticks(rotation=15)  # Rotate x-axis labels for readability
            plt.grid(True)
            # Improve date formatting on x-axis
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.tight_layout()
            file_name = f"{table}_{y_axis}.jpg"
            pickle_name = f"{table}_{y_axis}.pkl"
            file_path = os.path.join(test_files_path, file_name)
            pickle_path = os.path.join(test_files_path, pickle_name)
            plt.savefig(file_path)
            fig = plt.gcf()
            with open(pickle_path, "wb") as f:
                pickle.dump(fig, f)
            plt.close()


main()
