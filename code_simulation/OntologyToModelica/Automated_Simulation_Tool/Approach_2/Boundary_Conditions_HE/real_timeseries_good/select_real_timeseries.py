import xlrd
import os
import scipy as sci
import seaborn as sns
from modelicares import SimRes
from collections import OrderedDict
import datetime as dt
import numpy as np
import modelicares
import tkinter
from pyld import jsonld
from plotly.offline import plot
import plotly.graph_objects as go
import matplotlib
from ebc_sql import EbcSql 
import datetime
from pathlib import Path
import pandas as pd
import re
import csv


#--------------------------------list of weeks of the database-------------------
    
list_weeks=[]

final_date=datetime.datetime.strptime("2018-06-22","%Y-%m-%d")
u = datetime.datetime.strptime("2014-05-10","%Y-%m-%d")
d = datetime.timedelta(days=7)


while u<final_date:

    t = u + d
    list_weeks.append(t)
    u=t
    
    
    
#--------------------------------------------time series to download------------------------------------------
    
dict_ids=[
            {'name': 'T1',
             'itemID': 260,
             'plus': 273.15,
             'multiply': 1},
             
            {'name': 'T2',
             'itemID': 266,
             'plus': 273.15,
             'multiply': 1},
             
             {'name': 'T3',
             'itemID': 264,
             'plus': 273.15,
             'multiply': 1},
              
              {'name': 'T4',
             'itemID': 262,
             'plus': 273.15,
             'multiply': 1},
               
               {'name': 'm1',
             'itemID': 1755,
             'plus': 0,
             'multiply': 0.28},
                
                
                     {'name': 'm3',
             'itemID': 1754,
             'plus': 0,
             'multiply': 0.28}
                
             
         
        ]



#------Locate the time series that are not good for the algorithm. It is considered that the ones with standard deviation lower than 0.5 are removed

list_incorrect=[]

fig=go.Figure()

for i in list(range(0,197)):
    
    name_file_T1='T1_' + str(i) + '.mat'
    data_T1=sci.io.loadmat(name_file_T1)
    
    name_file_T2='T2_' + str(i) + '.mat'
    data_T2=sci.io.loadmat(name_file_T2)
    
    name_file_T3='T3_' + str(i) + '.mat'
    data_T3=sci.io.loadmat(name_file_T3)
    
    name_file_T4='T4_' + str(i) + '.mat'
    data_T4=sci.io.loadmat(name_file_T4)
    
    name_file_m1='m1_' + str(i) + '.mat'
    data_m1=sci.io.loadmat(name_file_m1)
    
    name_file_m3='m3_' + str(i) + '.mat'
    data_m3=sci.io.loadmat(name_file_m3)
    
    if np.std(data_T1['data'][:,1])<0.3 or np.std(data_T2['data'][:,1])<0.3 or np.std(data_T3['data'][:,1])<0.3 or np.std(data_T4['data'][:,1])<0.3:
        list_incorrect.append(i)
        
        fig.add_trace(go.Scatter(x=data_T2['data'][:,0], y=data_T2['data'][:,1], mode = 'lines'))
        fig.add_trace(go.Scatter(x=data_T4['data'][:,0], y=data_T4['data'][:,1], mode = 'lines'))
    
#---------------removing time series selected as incorrect------------------------------------

    
for i in list_incorrect:    
    os.remove("T1_" + str(i) + '.mat')
    os.remove("T2_" + str(i) + '.mat')
    os.remove("T3_" + str(i) + '.mat') 
    os.remove("T4_" + str(i) + '.mat') 
    os.remove("m1_" + str(i) + '.mat') 
    os.remove("m3_" + str(i) + '.mat') 


#----------------renumbering the time series once the incorrect ones have been removed---------------

    
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)     


j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith("T1_"):
        os.rename(filename, 'T1_' + str(j)+ '.mat')
        j=j+1


j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith('T2_'):
        os.rename(filename, 'T2_' + str(j) + '.mat')
        j=j+1
        
j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith('T3_'):
        os.rename(filename, 'T3_' + str(j) + '.mat')
        j=j+1

j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith('T4_'):
        os.rename(filename, 'T4_' + str(j) + '.mat')
        j=j+1
    
j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith('m1_'):
        os.rename(filename, 'm1_' + str(j) + '.mat')
        j=j+1
        
j=0
for filename in sorted_aphanumeric(os.listdir(".")):
    if filename.startswith('m3_'):
        os.rename(filename, 'm3_' + str(j) + '.mat')
        j=j+1
 