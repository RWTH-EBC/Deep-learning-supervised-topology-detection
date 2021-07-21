# Automated simulation tool

This is a tool for the automatation of the simulations with Dymola.

The different names of the approaches and the models can be better undertood by reading the Master Thesis of Belén Llopis.

It is important to have a copy of the repository of `AixLib` Modelica Library (from here: https://github.com/RWTH-EBC/AixLib) and install the Dymola-Python interface (here the indications: https://github.com/RWTH-EBC/AixLib/wiki/How-to:-Dymola-Python-Interface)


## Contents
The folder `Automated_Simulation_Tool`contains different elements.

### Approach_1
In this folder the tool takes numerical parameters to change in the model from al input matrix in a `.txt` file. It uses only one Modelica file `.mo`. 

### Approach_2
In this folder the tool takes different boundary conditions to change in the model from al input matrix in a `.txt` file. It creates only as much Modelica files `.mo` as simulations wants to be done, and executes one model by one. 


