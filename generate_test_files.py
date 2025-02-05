import os
import sys
import datetime
from datetime import timedelta
import random
import pandas as pd
import string
import re
import math
import pathlib


def string_cleaner(input):
    input = input.replace(",", "")
    input = input.replace("'", "")
    input = input.replace('"', "")
    return input


def sleep_tracking():
    """
    File structure: starting_timestamp,ending_timestamp,time_slept,comments
    DB structure: starting_timestamp,ending_timestamp,time_slept,comments
    """
    out = ""
    start = datetime.datetime.today()
    month = random.randint(1, 13)
    day = random.randint(1, 29)
    start = start.replace(
        hour=random.randint(20, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )
    end = start + timedelta(days=31)
    end = end.replace(hour=0, minute=0, second=0) - timedelta(seconds=1)
    curr = start
    while curr < end:
        starting_timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
        # let's assume person sleeps anywhere between 0 hours and 10 hours
        time_slept = random.randint(0, 36000)
        ending_timestamp = curr + timedelta(seconds=time_slept)
        ending_timestamp = ending_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        comment = "".join(
            random.choices(string.ascii_letters + string.punctuation, k=256)
        )
        comment = re.escape(comment)
        comment = string_cleaner(comment)
        out += "{},{},{},{}\n".format(
            starting_timestamp, ending_timestamp, time_slept, comment
        )
        curr += timedelta(seconds=random.randrange(86400))
    out = "starting_timestamp,ending_timestamp,time_slept,comments\n" + out
    return out


def historical_weight():
    """
    File structure: timestamp,weight
    DB structure: timestamp,weight
    """
    out = ""
    start, end = (
        datetime.datetime.today() - timedelta(days=30),
        datetime.datetime.today(),
    )
    curr = start
    weight = random.uniform(50, 100)
    while curr < end:
        if random.random() < 0.1:
            # the purpose of this is that there should be a 10% chance we don't record data for today (the idea of
            # missing day of recording data)
            continue
        else:
            timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
            weight = weight + random.uniform(-1, 1)
            height = random.uniform(0.5, 2.0)
            # bmi = weight / (height * height)  # we will calculate this at runtime
            out += "{},{:.1f}\n".format(timestamp, weight)
            curr += timedelta(seconds=random.randrange(86400))
    out = "timestamp,weight\n" + out
    return out


def food_tracking():
    """
    File structure: timestamp,meal_category,food_name,num_servings,mass,
                    vitaminA,vitaminC,vitaminD,vitaminE,iron,
                    sodium,carbohydrates,comments
    DB structure: timestamp,meal_category,food_name,num_servings,mass,
                    vitaminA,vitaminC,vitaminD,vitaminE,iron,
                    sodium,carbohydrates,comments
    """
    out = ""
    start, end = (
        datetime.datetime.today() - timedelta(days=30),
        datetime.datetime.today(),
    )
    curr = start
    while curr < end:
        if random.random() < 0.1:
            # the purpose of this is that there should be a 10% chance we don't record data for today (the idea of
            # missing day of recording data)
            continue
        else:
            for meal in ["breakfast", "lunch", "dinner"]:
                if random.random() < 0.1:
                    # user may forget to record this meal
                    pass
                else:
                    timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
                    meal_category = meal
                    food_name = "".join(random.choices(string.ascii_uppercase, k=100))
                    mass, serving_mass = random.uniform(10, 999), random.uniform(
                        10, 999
                    )
                    num_servings = mass / serving_mass
                    vitaminA, vitaminC, vitaminD, vitaminE = (
                        random.uniform(0, int(math.pow(2, 31))),
                        random.uniform(0, int(math.pow(2, 31))),
                        random.uniform(0, int(math.pow(2, 31))),
                        random.uniform(0, int(math.pow(2, 31))),
                    )
                    iron, sodium, carbohydrates = (
                        random.uniform(0, 99),
                        random.uniform(0, int(math.pow(2, 31))),
                        random.uniform(0, int(math.pow(2, 31))),
                    )
                    comment = "".join(
                        random.choices(string.ascii_letters + string.punctuation, k=256)
                    )
                    comment = re.escape(comment)
                    comment = string_cleaner(comment)
                    new_row = "{},{},{},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{:.1f},{}\n".format(
                        timestamp,
                        meal_category,
                        food_name,
                        num_servings,
                        mass,
                        vitaminA,
                        vitaminC,
                        vitaminD,
                        vitaminE,
                        iron,
                        sodium,
                        carbohydrates,
                        comment,
                    )
                    out += new_row
                    curr += timedelta(seconds=random.randrange(10800))  # approx 3hr
            curr += timedelta(seconds=random.randrange(36000))  # 10hr
    out = (
        "timestamp,meal_category,food_name,num_servings,mass,vitaminA,vitaminC,vitaminD,vitaminE,iron,sodium,carbohydrates,comments\n"
        + out
    )
    return out


def mood_tracking():
    """
    File structure: timestamp,happiness_rating,comments
    DB structure: timestamp,happiness_rating,comments
    """
    out = ""
    start, end = (
        datetime.datetime.today() - timedelta(days=30),
        datetime.datetime.today(),
    )
    curr = start
    while curr < end:
        if random.random() < 0.1:
            # the purpose of this is that there should be a 10% chance we don't record data for today (the idea of
            # missing day of recording data)
            continue
        else:
            timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
            happiness_rating = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            comment = "".join(
                random.choices(string.ascii_letters + string.punctuation, k=256)
            )
            comment = re.escape(comment)
            comment = string_cleaner(comment)
            out += "{},{:.1f},{}\n".format(timestamp, happiness_rating, comment)
            curr += timedelta(seconds=random.randrange(86400))
    out = "timestamp,happiness_rating,comments\n" + out
    return out


def exercise_tracking():
    """
    File structure: starting_timestamp,ending_timestamp,exercise_name,calories,reps,steps,comments
    DB structure: starting_timestamp,ending_timestamp,exercise_name,calories,reps,steps,comments
    """
    out = ""
    start, end = (
        datetime.datetime.today() - timedelta(days=30),
        datetime.datetime.today(),
    )
    curr = start
    while curr < end:
        if random.random() < 0.1:
            # the purpose of this is that there should be a 10% chance we don't record data for today (the idea of
            # missing day of recording data)
            continue
        else:
            starting_timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
            ending_timestamp = (
                curr + timedelta(seconds=random.randint(1, 86400))
            ).strftime("%Y-%m-%d %H:%M:%S")
            excercise_name = "".join(
                random.choices(string.ascii_letters + "-" + string.digits, k=20)
            )
            excercise_name = excercise_name.replace(",", "")
            calories = random.randint(1, 10000000)
            if random.randint(1, 10) > 8:
                reps = random.randint(1, 15)
            else:
                reps = ""
            if random.randint(1, 10) > 8:
                steps = random.randint(1, 100000)
            else:
                steps = ""
            comment = "".join(
                random.choices(string.ascii_letters + string.punctuation, k=256)
            )
            comment = re.escape(comment)
            comment = string_cleaner(comment)
            out += "{},{},{},{},{},{},{}\n".format(
                starting_timestamp,
                ending_timestamp,
                excercise_name,
                calories,
                reps,
                steps,
                comment,
            )
            curr += timedelta(seconds=random.randrange(86400))
    out = (
        "starting_timestamp,ending_timestamp,exercise_name,calories,reps,steps,comments\n"
        + out
    )
    return out


file_keys_to_function = {
    "historical_weight": historical_weight,
    "sleep_tracking": sleep_tracking,
    "food_tracking": food_tracking,
    "mood_tracking": mood_tracking,
    "exercise_tracking": exercise_tracking,
}


def main():
    curr_dir = pathlib.Path().resolve()
    for key in file_keys_to_function.keys():
        for i in range(1, 11):
            print(key, i)
            out = file_keys_to_function[key]()
            test_dir = os.path.join(curr_dir, "test_files")
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)
            fname = f"{key}_{i}.csv"
            fname = os.path.join(test_dir, fname)
            f = open(fname, "w")
            f.write(out)
            f.close()


main()
