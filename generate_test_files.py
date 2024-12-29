import os, sys
import datetime
from datetime import timedelta
import random
import pandas as pd
import string
import re

def sleep_tracking():
    """
    File structure: starting_timestamp, ending_timestamp, time_slept, comments
    DB structure: starting_timestamp, ending_timestamp, time_slept, comments
    """
    out = ""
    start = datetime.datetime.today()
    month = random.randInt(1,13)
    day = random.randInt(1,29)
    start = start.replace(hour=random.randInt(20,23), minute=random.randInt(0,60), second=random.randInt(0,60))
    end = start + timedelta(days=31)
    end = end.replace(hour=0,minute=0,second=0) - timedelta(seconds=1)
    curr = start
    while curr < end:
        starting_timestamp = curr.strftime("%Y-%m-%d %H:%M:%S")
        # let's assume person sleeps anywhere between 0 hours and 10 hours
        time_slept = random.randInt(0, 36000)
        ending_timestamp = curr + timedelta(seconds=time_slept)
        ending_timestamp = ending_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        comment = "".join(random.choices(string.ascii_letters + string.punctuation, k=256))
        comment = re.escape(comment)
        out += "{},{},{},{}\n".format(starting_timestamp, ending_timestamp, time_selpt, comment)
        curr += timedelta(days=1)
    return out

def historical_weight():
    """
    File structure: timestamp, weight
    DB structure: timestamp, weight, BMI
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
            while curr < end:
                dt = curr.strftime("%Y%m%d %H%M%S")
                weight = weight + random.uniform(-1, 1)
                out += "{},{:.1f}\n".format(dt, weight)
                curr += timedelta(days=1)
    return out


file_keys_to_function = {
    "historical_weight": historical_weight,
    "sleep_tracking": sleep_tracking,
}

def main():
    for key in file_keys_to_function.keys():
        for i in range(1,11):
            out = historical_weight()
            curr_dir = os.getcwd()
            fname = f"{key}_{i}.csv"
            fname = os.path.join(curr_dir, fname)
            f = open(fname, "w")
            f.write(out)
            f.close()
main()