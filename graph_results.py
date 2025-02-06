import os
import sys
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from datetime import timedelta
import random

all_tables_dict = {
    # "HISTORICAL_WEIGHT": ["weight", "bmi"],
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
    "EXERCISE_TRACKING": ["steps", "calories", "time_worked_out"],
}


height = random.uniform(1.4, 3.0)


def bmi_calculator(df):
    df["bmi"] = df["weight"] / (height * height)
    return df


def time_slept_to_hrs(df):
    df["time_slept_seconds"] = df["time_slept"]
    df["time_slept"] = df["time_slept"] / 3600
    return df


def time_worked_out(df):
    df["time_worked_out"] = (
        df["ending_timestamp"] - df["starting_timestamp"]
    ).total_seconds()
    return df


all_functions_dict = {
    "bmi": bmi_calculator,
    "time_slept": time_slept_to_hrs,
    "time_worked_out": time_worked_out,
}

conn = sqlite3.connect("test.db")


def main():
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
            sys.exit(1)
        for y_axis in all_tables_dict[table]:
            # for y_col in all_tables_dict["table"]:
            #     pass
            # data[x_col] = data[x_col].apply(
            #     lambda x: datetime.datetime.strptime(x, "%Y%m%d %H%M%S")
            # )
            # data[y_axis] = data[y_axis].apply(lambda x: int(x))
            if y_axis in all_functions_dict:
                update_df = all_functions_dict[y_axis]
                df = update_df(df)
            df[x_axis] = pd.to_datetime(df[x_axis], format="%Y-%m-%d %H:%M:%S")
            plt.figure(figsize=(10, 5))
            plt.plot(df[x_axis], df[y_axis], marker="o", linestyle="-")
            plt.xlabel("Date & Time")
            plt.ylabel(y_axis)
            plt.title(f"{y_axis.capitalize()} Graph")
            plt.xticks(rotation=45)  # Rotate x-axis labels for readability
            plt.grid(True)
            # Improve date formatting on x-axis
            plt.gca().xaxis.set_major_formatter(
                mdates.DateFormatter("%Y-%m-%d %H:%M")
            )  # Format labels
            plt.gca().xaxis.set_major_locator(
                mdates.AutoDateLocator()
            )  # Auto-adjust label frequency
            # Show the plot
            plt.show()
            # x_vals = df[x_col].values.tolist()
            # y_vals = df["weight"].values.tolist()
            # print(x_vals)
            # plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter())
            # plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
            # plt.plot(x_vals, y_vals)
            # # plt.gcf().autofmt_xdate()
            # plt.show()
            # data[x_col] = data[x_col].astype(str)
            # data[ts_col] = pd.to_datetime(data[ts_col], format="%Y%m%d %H%M%S")
            # data[ts_col] = data[ts_col].apply(
            #     lambda x: datetime.datetime.strptime(x, "%Y%m%d %H%M%S")
            # )
            # print(data)
            # data.plot(
            #     x="timestamp",
            #     y="weight",
            #     kind="scatter",
            # )  # xticks=xticks)
            # plt.show()
            # min_dt = min(data[ts_col])
            # # min_dt = datetime.datetime.strptime(min_dt, "%Y%m%d %H%M%S")
            # max_dt = max(data[ts_col])
            # # max_dt = datetime.datetime.strptime(max_dt, "%Y%m%d %H%M%S")
            # xticks = []
            # full_delta = (max_dt - min_dt).days
            # print(full_delta)
            # avg_delta = full_delta / 10
            # print(avg_delta)
            # while min_dt < max_dt:
            #     xticks.append(min_dt.strftime("%Y%m%d 000000"))
            #     # xticks.append(
            #     #     min_dt.replace(
            #     #         hour=0,
            #     #         minute=0,
            #     #     )
            #     # )
            #     min_dt = min_dt + timedelta(days=2)
            # # plt.plot(data["timestamp"], data["weight"])
            # # plt.xticks(xticks)
            # # print(data["timestamp"])
            # data.plot(
            #     x="timestamp",
            #     y="weight",
            #     # kind="scatter",
            # )  # xticks=xticks)
            # # plt.xticks(xticks)
            # plt.show()


main()
