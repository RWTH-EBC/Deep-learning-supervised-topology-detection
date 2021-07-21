import os
import modelicares
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dymola.dymola_interface import DymolaInterface
from dymola.dymola_exception import DymolaException
from plotly.offline import plot
import plotly.graph_objects as go
from pathlib import Path


##-----------------Function that generates the modelica files with the corresponding boundary conditions-----------------------------

#This function is very specific for this case. If another model is simulated, the names an itemID of the boundary conditions
#to change has to be manually modified here. For instance, in the Heat Pump folder can be seen how this is different. 

def generate_modelica_files_with_different_BC(indexes_dict, dict_input_simulation):

      for i in indexes_dict:
            
            f = open("Heat_Exchanger_new_model_2.txt",'r')
            file = f.read()
            f.close()
            
            file = file.replace('Heat_Exchanger_new_model_2', str(dict_input_simulation['names_output'][i]))
            file = file.replace('260', '260_' + dict_input_simulation['initial_values'][i][0])
            file = file.replace('264', '264_' + dict_input_simulation['initial_values'][i][1])
            file = file.replace('1755', '1755_' + dict_input_simulation['initial_values'][i][2])
            file = file.replace('1754', '1754_' + dict_input_simulation['initial_values'][i][3])
            file = file.replace('eps=0.7', 'eps=' + dict_input_simulation['initial_values'][i][4])

      
      
            f = open(str(dict_input_simulation['names_output'][i]) + '.txt','w')
            f.write(file)
            f.close()
      
       
      
      for filename in os.listdir("."):
            if filename.startswith("Simulation_"):
                  os.rename(filename, filename.split('.')[0] + '.mo')


#This function differs from the previous ones in that is creating the modelica files 
#using output results from simulations of other systems (the heat pump) as boundary conditions from this system.

def generate_connected_modelica_files_with_different_BC(indexes_dict, dict_input_simulation):

      for i in indexes_dict:
            
            f = open("Heat_Exchanger_new_model.txt",'r')
            file = f.read()
            f.close()
            
            file = file.replace('Heat_Exchanger_new_model', str(dict_input_simulation['names_output'][i]))
            file = file.replace('260', '260_' + dict_input_simulation['initial_values'][i][0])
            file = file.replace('1755', '1755_' + dict_input_simulation['initial_values'][i][0])
            file = file.replace('1754', 'm3_' + str(indexes_dict[i] + 1))
            file = file.replace('264', 'T3_' + str(indexes_dict[i] + 1))


            
      
      
            f = open(str(dict_input_simulation['names_output'][i]) + '.txt','w')
            f.write(file)
            f.close()
      
       
      
      for filename in os.listdir("."):
            if filename.startswith("Simulation_"):
                  os.rename(filename, filename.split('.')[0] + '.mo')


##-------------------function that performs simulation in dymola--------------------------------------------------------------------

def perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name):
# Start the interface
      dymola = DymolaInterface()
      


# Location of your local AixLib clone
      dir_aixlib = dir_aixlib_simulation


# Location where to store the results
      dir_result = dir_result_simulation


# Open AixLib and the model
      dymola.openModel(path=os.path.join(dir_aixlib, 'package.mo'))
      dymola.openModel(path=os.path.join(dir_result, list_names[i]))


# Translate any model you'd like to simulate
      dymola.translateModel(list_names[i].split('.')[0])

# Simulate the model
      output = dymola.simulateExtendedModel(
      problem=list_names[i].split('.')[0],
      startTime=0.0,
      stopTime=604800,
      outputInterval=300,
      method="dassl",
      tolerance=0.000001,
      resultFile=os.path.join(dir_result, 'Results_' + simulation_name + '_' +  str(list_names[i])),
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
            list_names.append('Simulation' + '_' + str(index + 1))

            dict_input_simulation={'names_output': list_names , 'initial_values': input_matrix_list }
      
      return dict_input_simulation



#-------------------------------------------------------------------------------------------------------------------------------------------
      
#---------------function that simulates in a loop all the input vectors from the input matrix----------------------------------------------
      
def loop_simulations(list_names, indexes_dict, dir_aixlib_simulation, dir_result_simulation, simulation_name):

      list_output_results=[]
      attempts_while_1=0
      attempts_while_2=0
      while_false=0

      list_output_errors=[]

      for i in indexes_dict:
            attempts_while_1=0
            attempts_while_2=0
            while_false=0
      
            output_simulation=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
      

            if output_simulation[0]==False:
      
                  while output_simulation[0]==False:
                        while_false=while_false+1
                        output_simulation=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                        print('Tried attempt  ' + str(while_false) + '  of while_false in ' + str(list_names[i]) + ' with input matix    ' + str(simulation_name))
                        if while_false>5: 
                              list_output_errors.append(i)
                              break
            
                  else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_2[0] < 200):
                              output_simulation=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                              attempts_while_1=attempts_while_1+1
                              print('Tried attempt  ' + str(attempts_while_1) + '  of attempts_while_1 in ' + str(list_names[i]) + ' with input matix    ' + str(simulation_name))
                              if attempts_while_1>4: 
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results.append(output_simulation)
                              
                        
            else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_2[0] < 200):
                              output_simulation=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                              attempts_while_2=attempts_while_2+1
                              print('Tried attempt  ' + str(attempts_while_2) + '  of attempts_while_2 in   ' + str(list_names[i]) + '   with input matix   ' + str(simulation_name) )
                              if attempts_while_2>4:
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results.append(output_simulation)

      return list_output_results, attempts_while_1, attempts_while_2, list_output_errors


#-------------------------------------------------------------------------------------------------------------------------------------------
      
#---------------function that simulates in a loop all the input vectors from the input matrix that failed in first loop----------------------------------------------
          
def loop_simulations_try_2(list_names, list_output_errors, dir_aixlib_simulation, dir_result_simulation, simulation_name):
                       
      list_output_results_try_2=[]
      attempts_while_1_try_2=0
      attempts_while_2_try_2=0
      while_false_2=0

      
      list_output_errors_try_2=[]
      
      for i in list_output_errors:
            attempts_while_1_try_2=0
            attempts_while_2_try_2=0
            while_false_2=0
            
            output_simulation_try_2=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
            
      
            if output_simulation_try_2[0]==False:
            
                  while output_simulation_try_2[0]==False:
                        while_false_2=while_false_2+1
                        output_simulation_try_2=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                        print('Tried attempt  ' + str(while_false_2) + '  of while_false_2 in ' + str(list_names[i]) + ' with input matix    ' + str(simulation_name))
                        if while_false_2>5: 
                              list_output_results_try_2.append(i)
                              break
                  
                  else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat'  , 'Temperature_Sensor2.T')
                        #(value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat'  , 'Temperature_Sensor2.T')
                        #(value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_2[0] < 200):
                              output_simulation_taguchi_try_2=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                              attempts_while_1_try_2=attempts_while_1_try_2+1
                              print('Tried attempt  ' + str(attempts_while_1_try_2) + '  of attempts_while_1 in ' + str(list_names[i]) + '    during try 2' + '   with input matix   ' + str(simulation_name) )
                              if attempts_while_1_try_2>4: 
                                    list_output_errors_try_2.append(i)
                                    break
                        else:
                              list_output_results_try_2.append(output_simulation_taguchi_try_2)
                              
                        
            else:
                        (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor4.T')
                        (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
                        #(value_sensor_1, time_sensor_1, mean_sensor_1)=load_sim_result(dir_result_simulation + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor1.T')
                        
                        while  (mean_sensor_4[0] < 200) or (mean_sensor_2[0] < 200):
                              output_simulation_taguchi_try_2=perform_simulation(list_names, i, dir_aixlib_simulation, dir_result_simulation, simulation_name)
                              attempts_while_2_try_2=attempts_while_2_try_2+1
                              print('Tried attempt  ' + str(attempts_while_2_try_2) + '  of attempts_while_2 in ' + str(list_names[i]) + '    during try 2'  + '   with input matix   ' + str(simulation_name))
                              if attempts_while_2_try_2>4:
                                    list_output_errors.append(i)
                                    break
                        else:
                              list_output_results_try_2.append(output_simulation_try_2)
      
      return list_output_results_try_2, attempts_while_1_try_2, attempts_while_2_try_2, list_output_errors_try_2


#------------------------------------------------------------------------------------------------------------------------------------
      
#------------Function that represents in plotly results of simulations---------------------------------------------------------------
      
def plot_with_plotly(name_folder, indexes_dict, dict_input_simulation, dir_result_simulation, simulation_name, list_names):
      
      p = Path("simulations_functions.py").resolve()
      p = str(p.parents[0])

      fig = go.Figure()      
      for i in indexes_dict:
            (value_sensor_4, time_sensor_4, mean_sensor_4)=load_sim_result(p + str(name_folder) + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor4.T')
            (value_sensor_2, time_sensor_2, mean_sensor_2)=load_sim_result(p + str(name_folder) + '\Results' + '_' + simulation_name + '_' +  str(list_names[i]) + '.mat' , 'Temperature_Sensor2.T')
            
            fig.add_trace(go.Scatter(x=time_sensor_4,
                                     y=value_sensor_4,
                                     mode='lines', 
                                     hoverinfo='x + y + text',
                                     text=str(dict_input_simulation['initial_values'][i]),  
                                     name='Sensor_4' + '_' + simulation_name + '_' +  str(i + 1)))
            
            fig.add_trace(go.Scatter(x=time_sensor_2,
                                     y=value_sensor_2, 
                                     mode='lines',  
                                     hoverinfo='x + y + text', 
                                     text=str(dict_input_simulation['initial_values'][i]),  
                                     name='Sensor_2' + '_' + simulation_name + '_' +  str(i + 1)))
            
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
