#!/usr/bin/env python3
# Example for how to extract model level data from file/fdb/polytope and create a time-hight plots. Note that fdb is only available on ECMWF atos.

# Import necessary libraries
import os
import earthkit.data as ekd
import pyfdb

from datetime import datetime, timedelta

def check_fdb_env():
    # Set FDB environment for atos
    os.environ["FDB_HOME"] = "/home/fdbtest"
    try:
        os.environ["FDB5_HOME"] = os.environ["ECMWF_TOOLBOX_DIR"]
    except:
        raise KeyError("Make sure to load ecmwf-toolbox before your start")


def fetch_data(request=None):

    if request is None:
        request = {
          "class": "d1",
          "dataset": "on-demand-extremes-dt",
          "stream": "oper",
          "expver": "test",
          "date": 20230820,
          "time": 3,
          "type": "fc",
          "levtype": "sfc",
          "georef": "u09tvk",
          "step": "1h15m",
          "param": 167,
        }

    print ("\nFetch data from FDB:\n ", request)
    data = ekd.from_source("fdb", request, read_all=True)
    return data, request


def change_and_write_data(data, modify={}):

    print ("\nModify data with:", modify)
    file1 = "test1.grib2"
    file2 = "test2.grib2"

    data.to_target("file", file1)

    set_values = ",".join(
        [f"{key}={value}" for key, value in modify.items() if value != ""]
    )

    cmd = "grib_set -s " + set_values + f" {file1} {file2}"
    os.system(cmd)

    return file2


def read_and_archive(filename):

    print ("\nRead file and archive to fdb")
    fdb = pyfdb.FDB()

    with open(filename, "rb") as infile:
        fdb.archive(infile.read())
    fdb.flush()


def main():

    user_georef = f"{os.environ["USER"]}xxxxx"[0:6]

    # Make sure FDB is correct
    check_fdb_env()

    # Fetch the example data and list
    data, request = fetch_data()
    print(data.ls(extra_keys=["georef"]))

    # Modify and dump the data
    modify = { "expver" : "zzzz", "georef" : user_georef }
    file_for_fdb = change_and_write_data(data, modify)

    # Read the data from disk and archive to FDB
    read_and_archive(file_for_fdb)

    # Get the data agin from FDB and list
    request.update(modify)
    data_new, request = fetch_data(request)
    print(data_new.ls(extra_keys=["georef"]))

    # Remove the new data from fdb
    wipe_request = request
    for key in ["levtype","step","param"]:
        wipe_request.pop(key)

    fdb_sel = ",".join(
        [f"{key}={value}" for key, value in wipe_request.items()]
    )
    cmd = f"fdb wipe {fdb_sel} --doit"
    print(f"\nClean FDB with command: {cmd}")
    os.system(cmd)

    # Try to get the data again
    print(f"\nTry to read from FDB again")
    data, request = fetch_data(request)
    print(data.ls())


if __name__ == "__main__":
    main()
