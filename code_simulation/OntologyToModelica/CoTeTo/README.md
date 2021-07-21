
This folder contains the most important scripts to run the tool.

Some information about its contents:

## Loaders

This is a python module package containing the data loaders. 

- BoundaryFile: Loads information from jsonld file and downloads the time series needed in case they are used as boundary conditions of the model.
- BudoFile: Loads jsonld file containing budo key, returns turtle file containing ontology based model. This is automatically showed in a Tkinter based environment and the data properties of the model can be added. 
- TurtleFile: Loads turtle file, return modelica file.

### Auxiliary

Folder `Auxiliary` contains needed Ontology `Brick.ttl`, `BrickFrame.ttl` and `BUDO-M.ttl`.

## ebc_jsonld_files

- JSON-LD AND BUDO-M ONTOLOGY (notebook and html): it explains how to use jsonld with BUDO-M ontology implemented everything in Python
- initial_jsonld.py: this is the input data of the tool. The code only takes it with this name (this has to be improved). In case another system is used (like the boiler) it should be changed inside this file. `initial_jsonld_boiler.py` and `initial_jsonld_heat-pump.py` are the examples of the boiler and the heat pump respectively that should be written for those systems inside the `initial_jsonld.py` file.
- The rest of files `xxxx_jsonld.py` are auxiliary info that was before in excel and it has been transformed into jsonld.

## Other important scripts

The other files are auxiliary for the tool. The main ones are:

### jsonld_budo_to_ontology

It is the main code of the tool. Everything is programed in this script.

### Interpreting_the_code_budo_to_ontology

In notebook and html, this file contains some notes about the original code `budo_to_ontology.py`, before the transformation of the input data from excel to jsonld.

### properties_tkinter

This python script is the substitution of the tool `OnWithData`. Now this file is imported in the `jsonld_budo_to_ontology.py` file and used as GUI for modifying the data before creating the Brick Model.


