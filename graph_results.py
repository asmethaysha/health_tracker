import os
import sys
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from datetime import timedelta

all_tables_dict = {
    "HISTORICAL_WEIGHT": ["weight", "bmi"],
    # "SLEEP_TRACKING",
    # "FOOD_TRACKING",
    # "MOOD_TRACKING",
    # "EXERCISE_TRACKING"
}


conn = sqlite3.connect("test.db")


def main():
    for table in all_tables_dict.keys():
        query = "SELECT * FROM {} order by timestamp ".format(table)
        df = pd.read_sql_query(query, conn)
        # x = [x[0] for x in data]
        # y = [y[1] for y in data]
        # plt.scatter(x, y)
        if "timestamp" in df.columns:
            x_col = "timestamp"
        elif "starting_timestamp" in df.columns:
            x_col = "starting_timestamp"
        else:
            print("ERROR")
            sys.exit(1)
        # for y_col in all_tables_dict["table"]:

        #     pass
        # data[x_col] = data[x_col].apply(
        #     lambda x: datetime.datetime.strptime(x, "%Y%m%d %H%M%S")
        # )
        # data["weight"] = data["weight"].apply(lambda x: int(x))
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d %H%M%S")
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["weight"], marker="o", linestyle="")
        plt.xlabel("Date & Time")
        plt.ylabel("Weight (kg)")
        plt.title("Weight Over Time")
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
