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



p = Path("download_real_timeseries.py").resolve()
p = str(p.parents[0])
outputpath=p

#----------------This function changes units adding or multiplying a factor-----------------
def convert_value (plus,multiply,value):
#altering units of data
    if plus!="nan":
        value=value+float(plus)
    if multiply!="nan":
        value=value*float(multiply)
    return value

#---------------This is the function that downloads time series and save them in mat file----------------

def load_mea_result(budo_key,itemID,time_start,time_end):
#loading measured data from databases
    path_to_config = os.path.join(os.path.dirname(os.path.realpath('__file__')),"res/settings_standard.ini")
    option_groups = "sql_from"
    connection = EbcSql(option_files=path_to_config,option_groups=option_groups)
    connection.set_standard(option_files=path_to_config,option_groups=["ts_database_from", "format"])
    time_start_df=dt.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")
    ids_ordered_dict = OrderedDict([(itemID,budo_key)])        
    data = connection.get_timeseries_df(ids=ids_ordered_dict,
                                        time_start=time_start,
                                        time_end=time_end,
                                        sort_by="ts_time_column",
                                        sort_order="ASC",
                                        use_query=True,
                                        get_last_value_before=True,
                                        replace_first_index=True)
    value_mea=data[budo_key]
    value_mea.index = (value_mea.index-time_start_df).total_seconds()
    time_mea=(data.index-time_start_df).total_seconds()
    time_mea_date_form = data.index
    return value_mea,time_mea,time_mea_date_form


#--------------------------------list of weeks of the database-------------------
    
list_weeks=[]

final_date=datetime.datetime.strptime("2018-06-22","%Y-%m-%d")
u = datetime.datetime.strptime("2014-05-10","%Y-%m-%d")
d = datetime.timedelta(days=7)


while u<final_date:

    t = u + d
    list_weeks.append(t)
    u=t
#-------------dictionary with the items of the data points to download ----------------------------------   

dict_ids=[
            {'BUDO': '',
             'itemID': 1025,
             'plus': 273.15,
             'multiply': 1},
             
            {'BUDO': '',
             'itemID': 1034,
             'plus': 273.15,
             'multiply': 1},
             
             {'BUDO': '',
             'itemID': 825,
             'plus': 0,
             'multiply': 0.01},
              
              {'BUDO': '',
             'itemID': 1036,
             'plus': 273.15,
             'multiply': 1},
               
               {'BUDO': '',
             'itemID': 1756,
             'plus': 0,
             'multiply': 0.28},
                
                  {'BUDO': '',
             'itemID': 1026,
             'plus': 273.15,
             'multiply': 1},
                   
                     {'BUDO': '',
             'itemID': 1757,
             'plus': 0,
             'multiply': 0.28}
             
             
         
        ]

#With the previous functions and dictionaries/lists, time series are downloaded

for i in list(range(0,len(list_weeks)-1)):
    time_start = str(list_weeks[i])
    time_end= str(list_weeks[i+1])
    
    
    for element in dict_ids:
        key=element['BUDO']
        itemID=int(element['itemID'])
        (value_mea,time_mea,time_mea_date_form)=load_mea_result(key,itemID,time_start,time_end) 
        value_mea=convert_value(float(element['plus']),float(element['multiply']),value_mea)
        matrix_name='data' 
        matrix=np.column_stack([value_mea.index, value_mea])
        output='/'.join(outputpath.split(".")[0].split('/')[0:-1])+'/'+str(element['itemID']) + '_' + str(i) +'.mat'
        sci.io.savemat(output,{matrix_name:matrix}) 


