#!/usr/bin/env python3
# Example for how to extract model level data from file/fdb/polytope and create a time-hight plots. 
# Note that fdb is only available on ECMWF atos.

# Import necessary libraries
import os
import earthkit.data
import pyfdb

from datetime import datetime, timedelta

def check_fdb_env():
    # Set FDB environment for atos
    os.environ["FDB_HOME"] = "/home/fdbtest"
    try:
        os.environ["FDB5_HOME"] = os.environ["ECMWF_TOOLBOX_DIR"]
    except:
        raise KeyError("Make sure to load ecmwf-toolbox before your start")


def get_georefs(datetime):
    date = datetime.strftime("%Y%m%d")
    time = datetime.strftime("%H")
    request = {
      "class": "d1",
      "dataset": "on-demand-extremes-dt",
      "expver": "0099",
      "date": date,
      "time": time,
      "param": 167,
      "step": 0,
    }
    recorded_georefs = {}
    for entry in pyfdb.list(request, keys=True):
      georef = entry["keys"]["georef"]
      if georef not in recorded_georefs:
        recorded_georefs[georef] = []
      stream = entry["keys"]["stream"]
      if stream not in recorded_georefs[georef]:
        recorded_georefs[georef].append(stream)

    return recorded_georefs

def timespan(days):
    end = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=days)
    return start, end

def print_georefs(start, end):

    # Loop over the period
    print(f"Search for runs for {start} to {end}")
    current = start
    while current < end:
        georefs = get_georefs(current)
        if len(georefs) > 0:
            print(f" {current}: {georefs}")
        current += timedelta(days=1)

def main():

    check_fdb_env()

    start, end = timespan(days=5)
    print_georefs(start, end)

if __name__ == "__main__":
    main()
