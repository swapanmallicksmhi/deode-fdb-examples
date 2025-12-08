# DEODE fdb examples
In the following we give a few examples on howto work with fdb from python.

## Important information about experiment identifiers
In some of the examples we modify the experiment identifier `expver` as a test. For your own future archiving NEVER pick random expver but please do as below to get a new expver. The general convention is to use numerical identifiers for operations, e.g. 0001, and alpha numerical ones for research, i.e. personal runs. The utility `getNewId` will simply increment to a new id everytime it's called.

```
module load pifsenv
getNewId -g d1.on-demand-extremes-dt
```

## Install

To install the required environment e.g. locally do, in this case with micromamba, and preferred python version

```
micromamba create -n deode_fdb_examples python=3.12
micromamba env update -n deode_fdb_examples -f environment.yml
```

## Activate and load the correct EcCodes 
```
micromamba activate deode_fdb_examples
module load ecmwf-toolbox/2025.10.1.0
```

## List example
List available georefs and corresponding streams from FDB for the past 5 days. Note that we used stream = oper/enfo for deterministic/ensemble runs respectively

```
python3 ./find_georef.py
```

## Read write example
Example to read data from FDB, change expver and georef, and archive again.

```
python3 ./read_and_write.py
```


## Example to read data from FDB for a certain date, expver and georef

```
python3 ./fdb_search.py
```
