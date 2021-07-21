
import os
import modelicares
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dymola.dymola_interface import DymolaInterface
from plotly.offline import plot
import plotly.graph_objects as go
from simulations_functions import perform_simulation, load_sim_result, dictionary_input_simulation, loop_simulations, loop_simulations_try_2, plot_with_plotly, generate_modelica_files_with_different_BC, generate_connected_modelica_files_with_different_BC
from pathlib import Path
import time
import shutil
import datetime

#------------Setting paths of Aixlib and working directory----------------------------------------------------------------------------------------------------------------

#Path to "package.mo" file from Aixlib library to load it.

dir_aixlib_simulation=r'F:\AixLib\AixLib\AixLib'

#Path where this script is. It should be in the same folder as the modelica model and its .mat boundary conditions (e.g. 825.mat, 1026.mat, ...) and the input_matrix text file.
p = Path("dymola_python_simulations.py").resolve() 
p = p.parents[0]
dir_result_simulation=str(p) 

#-------------------------------------------------------------------------------------------------------------------------------------------

#Generating the modelica files 

input_matrix_taguchi = np.genfromtxt('input_matrix_taguchi_test_3.txt',  dtype='str')
dict_input_simulation_taguchi=dictionary_input_simulation(input_matrix_taguchi)
indexes_dict_taguchi=list(range(0,len(dict_input_simulation_taguchi['initial_values'])))

#Choose this function depending on the boundary conditions (output from other simulations or not) are used.
generate_modelica_files_with_different_BC(indexes_dict_taguchi, dict_input_simulation_taguchi)
#generate_modelica_files_with_different_BC(indexes_dict_taguchi, dict_input_simulation_taguchi)


#-----------------Simulation Taguchi matrix-------------------------------------------------------------------------------------------------

input_matrix_taguchi = np.genfromtxt('input_matrix_taguchi_test_3.txt',  dtype='str')

simulation_name_taguchi='taguchi'

dict_input_simulation_taguchi=dictionary_input_simulation(input_matrix_taguchi)

indexes_dict_taguchi=list(range(0,len(dict_input_simulation_taguchi['initial_values'])))

list_names_taguchi=dict_input_simulation_taguchi['names_output']

start=time.time()



list_output_results_taguchi, attempts_while_1_taguchi, attempts_while_2_taguchi, list_output_errors_taguchi = loop_simulations (list_names_taguchi, 
                                                                                                                                indexes_dict_taguchi, 
                                                                                                                                dir_aixlib_simulation, 
                                                                                                                                dir_result_simulation, 
                                                                                                                                simulation_name_taguchi)




list_output_results_try_2_taguchi, attempts_while_1_try_2_taguchi, attempts_while_2_try_2_taguchi, list_output_errors_try_2_taguchi=loop_simulations_try_2(list_names_taguchi, 
                                                                                                                                                           list_output_errors_taguchi, 
                                                                                                                                                           dir_aixlib_simulation, 
                                                                                                                                                          dir_result_simulation, 
                                                                                                                                                           simulation_name_taguchi)


#The loops for simulations are repeated by using the ones that gave errors in the previous simulations.

indexes_dict_taguchi=list_output_errors_try_2_taguchi





list_output_results_taguchi, attempts_while_1_taguchi, attempts_while_2_taguchi, list_output_errors_taguchi = loop_simulations (list_names_taguchi, 
                                                                                                                                indexes_dict_taguchi, 
                                                                                                                                dir_aixlib_simulation, 
                                                                                                                                dir_result_simulation, 
                                                                                                                                simulation_name_taguchi)




list_output_results_try_2_taguchi, attempts_while_1_try_2_taguchi, attempts_while_2_try_2_taguchi, list_output_errors_try_2_taguchi=loop_simulations_try_2(list_names_taguchi, 
                                                                                                                                                           list_output_errors_taguchi, 
                                                                                                                                                           dir_aixlib_simulation, 
                                                                                                                                                           dir_result_simulation, 
                                                                                                                                                           simulation_name_taguchi)




end=time.time()



print('The simulation took  ' + str(datetime.timedelta(seconds=(end-start))))


name_folder_taguchi=""

fig_taguchi= plot_with_plotly(name_folder_taguchi, indexes_dict_taguchi, dict_input_simulation_taguchi, dir_result_simulation, simulation_name_taguchi, list_names_taguchi)

