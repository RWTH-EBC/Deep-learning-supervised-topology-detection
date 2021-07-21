# Download the real time series of the case

There are 2 scripts for this: `ebc_sql.py` and `download_real_timeseries.py`.

`Res` folder contains settigs for `ebc_sql.py`, so it is also needed.



## ebc_sql

This script has the tools for downloading the time series from the data base. It is from this folder: https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/master/dataset

## download_real_timeseries

This script uses the function `load_mea_result` that uses `ebc_sql` for downloading the time series and save it into a .mat file.

It is used the `list_weeks` for creating the week periods that wants to be downloaded, and `dict_ids` for the names of the variables and itemID.