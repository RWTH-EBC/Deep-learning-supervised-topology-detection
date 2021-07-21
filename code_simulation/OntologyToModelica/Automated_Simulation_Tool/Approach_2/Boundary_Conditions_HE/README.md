# Instructions

There are 2 scripts for simulating: `dymola_python_simulations.py` and `simulations_functions.py`.

This files are used in all cases but each case has its own modifications.

In the same folder there has to be:
- boundary conditions (e.g. 1756_A.mat, 1756_B.mat, ...) and if it is required boundary conditions from other simulations (e.g. T3_1.mat, T3_2-mat,...)
- Modelica model (e.g. HeatExchanger.mo) and the same model in .txt file (e.g. HeatPump.txt)
- input matrix (e.g. input_matrix.txt)

There are also 2 folders, that are used for downloading the real time series from the data base:

- real_timeseries_all
- real_timeseries_good


## simulations_functions
This script contains the functions used for simulation. The code contains notations about its usage. The functions are:

- generate_modelica_files_with_different_BC: this function takes the input matrix and generates the modelica models of each case os the matrix with its different boundary conditions.
- generate_connected_modelica_files_with_different_BC: this function does the same as the previous one but taking as boundary conditions results from other simulations (if it is specified in the matrix).
- perform_simulation: this is the function that makes the simulation. It is specified inside the settings of this case.
- load_sim_result: loads the results from the `.mat` file created with Dymola.
- dictionary_input_simulation: creates a dictionary with the information from the input matrix.
- loop_simulations: takes the `perform_simulation` function and repeats each case until the output result is `True` and the result temperatures are consisten.
- loop_simulations_try_2: repeats the same as `loop_simulation` but with the cases that did not succeed bedore.
- plot_with_plotly: plots the results in plot.ly to be able to identify if there are mistakes.

## dymola_python_simulations

This scripts implements the functions for each case, where are defined the name of the variables and the paths for simulating. 