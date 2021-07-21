# ontology based model to modelica model generation tool
This is a tool for the generation of modelica model from ontology based model. 
This is the adaptation and improvements to the tool started by Yingying Yang.
The tool is deveploped based on **CoTeTo** - Code Templating Tool.
It can be accessed through Github:
https://github.com/UdK-VPT/CoTeTo 

## Contents
The folder `OntologyToModelica`contains different elements.

### Automated_Simulation_Tool
Here are the scripts used to simulate the model created with the tool automatically changing the parameters from an input matrix. 

It is not implemented inside CoTeTo, it works independently with scripts including functions that take the Modelica model `.mo` created with the tool.

### CoTeTo
This is the main python module package of the tool. 
`jsonld_budo_to_ontology.py` file contains the functions used to generate budo key to ontology based model. It is also used the script `properties_tkinter.py` to create the environment that allows to introduce the values and data properties of the model. 


### Generators
This folder contains the generators. 
- BouGen: downloads real time series from the data base, in case the user wants to use them as boundary conditions of the model.
- BuToOn: generate ontology based model from budo key
- OnToMo: generate modelica model from ontology based model. File "function.mao" contains needed functions for generation of modelica models.
- ResPlot: plots the results of the simulated model and the real time series for comparision and validation.

### Scripts
**This file has the main script that starts the tool**.
It gives an interface to this tool in a graphical environment with `CoTeTo_gui.py`. 

### tools
Script from CoTeTo needed to run the tool.


# other package needed
To run the code, the following packages need to be installed (under `Python 3.6` with `Anaconda Navigator`):
- rdflib
- StyleFrame
- mako
- xlrd
- PyQt5
- configparser
- argparse
- logging
- importlib
- modelicares
- pymysql
- buildingspy
- pyqtwebengine
- PyLD
- Tkinter



