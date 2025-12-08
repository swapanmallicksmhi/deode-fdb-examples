#
# Extract given date(s), georef and param(s)
# for levtype=sfc from FDB
#

import os
import pyfdb
import shutil

from tools import check_fdb_env

USER = os.environ["USER"]

def get_data(date, georef, param=None, step=None):
    request1 = {
        "class": "d1",
        "dataset": "on-demand-extremes-dt",
        "expver": "0099",
        "date": date,
        "time": 0,
        "levtype": "sfc",
        "georef": georef,
        "param": param,
    }

    requests = [ request1 ]
    if param is None:
        request1.pop("param")
    if step is not None:
        if isinstance(step,str):
            steps = [step]
        else:
            steps = step
        requests = []
        request2 = request1.copy()
        print(steps)
        for _step in steps:
          request1["step"] = _step
          requests.append(request1)
          if _step > 0 :
            request2["step"] = f"0-{_step}"
            requests.append(request2)

    name = "_".join([str(x) for x in requests[0].values() if isinstance(x, (str, int))])
    filename = f"/scratch/{USER}/{name}.grib2"

    j = 0
    with open(filename, "wb") as o:
        for request in requests:
         print("Handle:", request)
         for x in pyfdb.list(request, keys=True):
            y = x["keys"]
            i = pyfdb.retrieve(y)
            shutil.copyfileobj(i, o)
            if j % 10:
                pyfdb.flush()
            j += 1

    print(f"Data written to {filename}")


def main():

    check_fdb_env()
    # Example with several parameters and one step
    #get_data(date=20241119, georef="ud3q9t", param=[134,144,151,165,166,167,168,169,175,228164,228228,260046],step=1)
    # Example with all parameters and selected steps
    #get_data(date=20241119, georef="ud3q9t", step=[2,3])
    # This is an ensemble case 
    get_data(date=20251205, georef="sw7rm9", step = [2,3], param = [167])

if __name__ == "__main__":
    main()

