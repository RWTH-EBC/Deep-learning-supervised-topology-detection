# Select the real time series that have good quality

There is one script for this: `select_real_timeseries.py`.



## select_real_timeseries

This file works after all the real time series from the folder `real_timeseries_all` are copied here. 

This script locates the ones that are not good and deletes and renumbers them. In this case, the criteria used for deleting the time series is if the standard deviation of the whole week of any of the variables is lower than 0.5, then it is deleted.
