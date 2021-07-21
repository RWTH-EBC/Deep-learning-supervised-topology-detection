

import os
import modelicares
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dymola.dymola_interface import DymolaInterface
from plotly.offline import plot
import plotly.graph_objects as go
from simulations_functions import perform_simulation, load_sim_result, dictionary_input_simulation, loop_simulations, loop_simulations_try_2, plot_with_plotly
from pathlib import Path

#------------Setting paths and modelica model----------------------------------------------------------------------------------------------------------------

#Set the path of Aixlib "package.mo" file to load it.
dir_aixlib_simulation = r'C:\Users\Juan\sciebo\MT\AixLib\AixLib\AixLib' 

#Path where this script is. It should be in the same folder as the modelica model and its .mat boundary conditions (e.g. 825.mat, 1026.mat, ...) and the input_matrix text file.
p = Path("dymola_python_simulations_B.py").resolve() 
p = p.parents[0]
dir_result_simulation=str(p) 

#Modelica model file with the extension .mo that wants to be simulated.
mod_name_A='HeatPump_Bou_B.mo' 

#-------------------------------------------------------------------------------------------------------------------------------------------


#-----------------Simulation Taguchi matrix-------------------------------------------------------------------------------------------------

input_matrix_taguchi = np.loadtxt('input_matrix_taguchi.txt', usecols=range(5))

simulation_name_taguchi='taguchi'

dict_input_simulation_taguchi=dictionary_input_simulation(input_matrix_taguchi)

indexes_dict_taguchi=list(range(0,len(dict_input_simulation_taguchi['initial_values'])))

#indexes_dict_taguchi=[12]



list_output_results_taguchi, attempts_while_1_taguchi, attempts_while_2_taguchi, list_output_errors_taguchi = loop_simulations (mod_name_A, 
                                                                                                                            indexes_dict_taguchi, 
                                                                                                                            dir_aixlib_simulation, 
                                                                                                                            dir_result_simulation, 
                                                                                                                            dict_input_simulation_taguchi, 
                                                                                                                            simulation_name_taguchi)

list_output_results_try_2_taguchi, attempts_while_1_try_2_taguchi, attempts_while_2_try_2_taguchi, list_output_errors_try_2_taguchi=loop_simulations_try_2(mod_name_A, 
                                                                                                                                                          list_output_errors_taguchi, 
                                                                                                                                                          dir_aixlib_simulation, 
                                                                                                                                                          dir_result_simulation, 
                                                                                                                                                          dict_input_simulation_taguchi, 
                                                                                                                                                          simulation_name_taguchi)

name_folder_taguchi=r'\taguchi'

fig_taguchi= plot_with_plotly(name_folder_taguchi, indexes_dict_taguchi, dict_input_simulation_taguchi, dir_result_simulation, simulation_name_taguchi)






#-------------------------2 level full factorial design 1-------------------------------------------------------------------

input_matrix_full_factorial_1 = np.loadtxt('input_matrix_full_factorial.txt', usecols=range(5))

simulation_name_full_factorial_1='full_factorial'

dict_input_simulation_full_factorial_1=dictionary_input_simulation(input_matrix_full_factorial_1)

indexes_dict_full_factorial_1=list(range(0,len(dict_input_simulation_full_factorial_1['initial_values'])))

#indexes_dict_full_factorial_1=[12]




list_output_results_full_factorial_1, attempts_while_1_full_factorial_1, attempts_while_2_full_factorial_1, list_output_errors_full_factorial_1 = loop_simulations (mod_name_A, 
                                                                                                                            indexes_dict_full_factorial_1, 
                                                                                                                            dir_aixlib_simulation, 
                                                                                                                            dir_result_simulation, 
                                                                                                                            dict_input_simulation_full_factorial_1, 
                                                                                                                            simulation_name_full_factorial_1)

list_output_results_try_2_full_factorial_1, attempts_while_1_try_2_full_factorial_1, attempts_while_2_try_2_full_factorial_1, list_output_errors_try_2_full_factorial_1=loop_simulations_try_2(mod_name_A, 
                                                                                                                                                          list_output_errors_full_factorial_1, 
                                                                                                                                                          dir_aixlib_simulation, 
                                                                                                                                                          dir_result_simulation, 
                                                                                                                                                          dict_input_simulation_full_factorial_1, 
                                                                                                                                                          simulation_name_full_factorial_1)

name_folder_full_factorial_1=r'\FFD_1'
#name_folder_full_factorial_1=r''


fig_full_factorial_1= plot_with_plotly(name_folder_full_factorial_1, indexes_dict_full_factorial_1, dict_input_simulation_full_factorial_1, dir_result_simulation, simulation_name_full_factorial_1)



#-------------------------2 level full factorial design 2-------------------------------------------------------------------


input_matrix_full_factorial_2 = np.loadtxt('input_matrix_full_factorial_2.txt', usecols=range(5))

simulation_name_full_factorial_2='full_factorial_2'

dict_input_simulation_full_factorial_2=dictionary_input_simulation(input_matrix_full_factorial_2)

indexes_dict_full_factorial_2=list(range(0,len(dict_input_simulation_full_factorial_2['initial_values'])))

#indexes_dict_full_factorial_2=[12]




list_output_results_full_factorial_2, attempts_while_1_full_factorial_2, attempts_while_2_full_factorial_2, list_output_errors_full_factorial_2 = loop_simulations (mod_name_A, 
                                                                                                                            indexes_dict_full_factorial_2, 
                                                                                                                            dir_aixlib_simulation, 
                                                                                                                            dir_result_simulation, 
                                                                                                                            dict_input_simulation_full_factorial_2, 
                                                                                                                            simulation_name_full_factorial_2)

list_output_results_try_2_full_factorial_2, attempts_while_1_try_2_full_factorial_2, attempts_while_2_try_2_full_factorial_2, list_output_errors_try_2_full_factorial_2=loop_simulations_try_2(mod_name_A, 
                                                                                                                                                          list_output_errors_full_factorial_2, 
                                                                                                                                                          dir_aixlib_simulation, 
                                                                                                                                                          dir_result_simulation, 
                                                                                                                                                          dict_input_simulation_full_factorial_1, 
                                                                                                                                                          simulation_name_full_factorial_2)

name_folder_full_factorial_2=r'\FFD_2'

fig_full_factorial_2= plot_with_plotly(name_folder_full_factorial_2, 
                                       indexes_dict_full_factorial_2, 
                                       dict_input_simulation_full_factorial_2, 
                                       dir_result_simulation, 
                                       simulation_name_full_factorial_2)



#-------------------------Box and Behnken-------------------------------------------------------------------------------


input_matrix_BB = np.loadtxt('input_matrix_BB.txt', usecols=range(5))

simulation_name_BB='Box_Behnken'

dict_input_simulation_BB=dictionary_input_simulation(input_matrix_BB)

indexes_dict_BB=list(range(0,len(dict_input_simulation_BB['initial_values'])))

#indexes_dict_BB=[12]




list_output_results_BB, attempts_while_1_BB, attempts_while_2_BB, list_output_errors_BB = loop_simulations (mod_name_A, 
                                                                                                            indexes_dict_BB, 
                                                                                                            dir_aixlib_simulation, 
                                                                                                            dir_result_simulation, 
                                                                                                            dict_input_simulation_BB, 
                                                                                                            simulation_name_BB)

list_output_results_try_2_BB, attempts_while_1_try_2_BB, attempts_while_2_try_2_BB, list_output_errors_try_2_BB=loop_simulations_try_2(mod_name_A, 
                                                                                                                                       list_output_errors_BB, 
                                                                                                                                       dir_aixlib_simulation, 
                                                                                                                                       dir_result_simulation, 
                                                                                                                                       dict_input_simulation_full_factorial_1, 
                                                                                                                                       simulation_name_BB)

name_folder_BB=r'\BB'

fig_BB= plot_with_plotly(name_folder_BB, 
                         indexes_dict_BB, 
                         dict_input_simulation_BB, 
                         dir_result_simulation, 
                         simulation_name_BB)


