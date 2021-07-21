
import os
import modelicares
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dymola.dymola_interface import DymolaInterface
from plotly.offline import plot
import plotly.graph_objects as go
from pathlib import Path


##-------------------function that performs simulation in dymola------------------------------

def perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name):
# Start the interface
      dymola = DymolaInterface()

# Location of your local AixLib clone
      dir_aixlib = dir_aixlib_simulation


# Location where to store the results
      dir_result = dir_result_simulation


# Open AixLib
      dymola.openModel(path=os.path.join(dir_aixlib, 'package.mo'))
      dymola.openModel(path=os.path.join(dir_result, mod_name))


# Translate any model you'd like to simulate
      dymola.translateModel(mod_name.split('.')[0])

# Simulate the model
      output = dymola.simulateExtendedModel(
      problem=mod_name.split('.')[0],
      startTime=0.0,
      stopTime=604800,
      outputInterval=300,
      method="dassl",
      tolerance=0.000001,
      resultFile=os.path.join(dir_result, 'HeatPump_Bou_results' + '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1)),
      initialNames = ["Heat_Pump1.dTEva_nominal", "Heat_Pump1.dTCon_nominal", "Heat_Pump1.dp1_nominal", "Heat_Pump1.dp2_nominal", "Heat_Pump1.P_nominal"],
      initialValues = dict_input_simulation['initial_values'][i],
      finalNames=['Temperature_Sensor1.T', 'Temperature_Sensor2.T', 'Temperature_Sensor3.T', 'Temperature_Sensor4.T'],
   
      )

      dymola.close()
      
      
      return output

#----------------------------------------------------------------------------------------------------------------------------------------------
      
#------function that loads results from simulation with modelicares---------------------------------------------------------------------------

def load_sim_result(simrespath,variable):
#loading simulation results
    sims, __ = modelicares.load(simrespath)
    value_sim = sims[variable].values()
    time_sim=sims[variable].times()
    mean_sim=sims[variable].mean()
    value_sim=value_sim[0]
    time_sim=time_sim[0]
    
    return value_sim,time_sim, mean_sim

#------------------------------------------------------------------------------------------------------------------------------------------
    
#---------------function that creates a dictionary from the input matrix with names and values for simulation------------------------------
    
def dictionary_input_simulation(input_matrix):

      input_matrix_list=input_matrix.tolist()

      indexes=list(range(0,len(input_matrix)))

      list_names=[]

      for index in indexes:
            list_names.append(['Temperature_Sensor1.T' + '_' + 'simulation' + '_' +  str(index + 1), 'Temperature_Sensor2.T' + '_' + 'simulation' + '_' +  str(index  + 1), 'Temperature_Sensor3.T' + '_' + 'simulation' + '_' +  str(index  + 1), 'Temperature_Sensor4.T' + '_' + 'simulation' + '_' +  str(index + 1)])

            dict_input_simulation={'names_output': list_names , 'initial_values': input_matrix_list }
      
      return dict_input_simulation



#-------------------------------------------------------------------------------------------------------------------------------------------
      
#---------------function that simulates in a loop all the input vectors from the input matrix----------------------------------------------
      
def loop_simulations(mod_name, indexes_dict, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name):

      list_output_results=[]
      attempts_while_1=0
      attempts_while_2=0

      list_output_errors=[]

      for i in indexes_dict:
            attempts_while_1=0
            attempts_while_2=0
      
            output_simulation=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
      

            if output_simulation[0]==False:
      
                  while output_simulation[0]==False:
                        print('Output result False. It is tried again.')
                        output_simulation=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                  
            
                  else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_3, time_sensor_3, mean_sensor_3)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor3.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor2.T')
                        (value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_3[0] < 200) or (mean_sensor_2[0] < 200) or (mean_sensor_1[0] < 200):
                              output_simulation=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                              attempts_while_1=attempts_while_1+1
                              print('Tried attempt  ' + str(attempts_while_1) + '  of attempts_while_1 in simulation number  ' + str(i+1) + '     with input matix    ' + str(simulation_name))
                              if attempts_while_1>1: 
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results.append(output_simulation)
                              
                        
            else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_3, time_sensor_3, mean_sensor_3)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor3.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor2.T')
                        (value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_3[0] < 200) or (mean_sensor_2[0] < 200) or (mean_sensor_1[0] < 200):
                              output_simulation=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                              attempts_while_2=attempts_while_2+1
                              print('Tried attempt  ' + str(attempts_while_2) + '  of attempts_while_2 in simulation number  ' + str(i+1) + '   with input matix   ' + str(simulation_name) )
                              if attempts_while_2>1:
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results.append(output_simulation)

      return list_output_results, attempts_while_1, attempts_while_2, list_output_errors


#-------------------------------------------------------------------------------------------------------------------------------------------
      
#---------------function that simulates in a loop all the input vectors from the input matrix that failed in first loop----------------------------------------------
          
def loop_simulations_try_2(mod_name, list_output_errors, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name):
                       
      list_output_results_try_2=[]
      attempts_while_1_try_2=0
      attempts_while_2_try_2=0
      
      list_output_errors_try_2=[]
      
      for i in list_output_errors:
            attempts_while_1_try_2=0
            attempts_while_2_try_2=0
            
            output_simulation_try_2=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
            
      
            if output_simulation_try_2[0]==False:
            
                  while output_simulation_try_2[0]==False:
                        output_simulation_taguchi_try_2=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                        
                  
                  else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_3, time_sensor_3, mean_sensor_3)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor3.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor2.T')
                        (value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_3[0] < 200) or (mean_sensor_2[0] < 200) or (mean_sensor_1[0] < 200):
                              output_simulation_taguchi_try_2=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                              attempts_while_1_try_2=attempts_while_1_try_2+1
                              print('Tried attempt  ' + str(attempts_while_1_try_2) + '  of attempts_while_1 in simulation number  ' + str(i+1) + '    during try 2' + '   with input matix   ' + str(simulation_name) )
                              if attempts_while_1_try_2>1: 
                                    list_output_errors_try_2.append(i)
                                    break
                        else:
                              list_output_results_try_2.append(output_simulation_taguchi_try_2)
                              
                        
            else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_3, time_sensor_3, mean_sensor_3)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor3.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor2.T')
                        (value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\HeatPump_Bou_results' +  '_' + 'simulation' + '_' + simulation_name + '_' +  str(i + 1) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_3[0] < 200) or (mean_sensor_2[0] < 200) or (mean_sensor_1[0] < 200):
                              output_simulation_taguchi_try_2=perform_simulation(mod_name, i, dir_aixlib_simulation, dir_result_simulation, dict_input_simulation, simulation_name)
                              attempts_while_2_try_2=attempts_while_2_try_2+1
                              print('Tried attempt  ' + str(attempts_while_2_try_2) + '  of attempts_while_2 in simulation number  ' + str(i+1) + '    during try 2'  + '   with input matix   ' + str(simulation_name))
                              if attempts_while_2_try_2>1:
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results_try_2.append(output_simulation_try_2)
      
      return list_output_results_try_2, attempts_while_1_try_2, attempts_while_2_try_2, list_output_errors_try_2


#------------------------------------------------------------------------------------------------------------------------------------
      
#------------Function that represents in plotly results of simulations---------------------------------------------------------------
      
def plot_with_plotly(name_folder, indexes_dict, dict_input_simulation, dir_result_simulation, simulation_name):
      
      p = Path("simulations_functions.py").resolve()
      p = str(p.parents[0])

      fig = go.Figure()      
      for i in indexes_dict:
            (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(p + str(name_folder) + '\HeatPump_Bou_results_simulation_' + simulation_name + '_' +  str(i + 1) + '.mat', 'Temperature_Sensor4.T')
            (value_sensor_3, time_sensor_3, mean_sensor_3)=load_sim_result(p + str(name_folder) + '\HeatPump_Bou_results_simulation_' + simulation_name + '_' +  str(i + 1) + '.mat', 'Temperature_Sensor3.T')
            
            fig.add_trace(go.Scatter(x=time_sensor_4,
                                     y=value_sensor_4,
                                     mode='lines', 
                                     hoverinfo='x + y + text',
                                     text=str(dict_input_simulation['initial_values'][i]),  
                                     name='Sensor_4' + '_' + simulation_name + '_' +  str(i + 1)))
            
            fig.add_trace(go.Scatter(x=time_sensor_3,
                                     y=value_sensor_3, 
                                     mode='lines',  
                                     hoverinfo='x + y + text', 
                                     text=str(dict_input_simulation['initial_values'][i]),  
                                     name='Sensor_3' + '_' + simulation_name + '_' +  str(i + 1)))
            
            fig.update_layout(
                        title=go.layout.Title(
                                                text=str(simulation_name),
                                                xref="paper",
                                                x=0.5
                                                ),
                        xaxis=go.layout.XAxis(
                                                title=go.layout.xaxis.Title(
                                                            text="Time [s]",
                                                            font=dict(
                                                                family="Courier New, monospace",
                                                                size=18,
                                                                color="#7f7f7f"
                                                            )
                                                        )
                                                    ),
                        yaxis=go.layout.YAxis(
                                                title=go.layout.yaxis.Title(
                                                                  text="T [K]",
                                                                  font=dict(
                                                                      family="Courier New, monospace",
                                                                      size=18,
                                                                      color="#7f7f7f"
                                                                                                      )
                                                                                                  )
                                                                                              )
                                                                                          )
            fig.update_yaxes(range=[200, 400])   
      plot(fig)
      
      return fig


