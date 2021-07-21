from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from StyleFrame import StyleFrame 
from openpyxl import load_workbook
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
import json
import pprint

#When using CoTeTo GUI

from CoTeTo.ebc_sql import EbcSql
from CoTeTo.ebc_jsonld_files.initial_jsonld import context
from CoTeTo.ebc_jsonld_files.initial_jsonld import doc
from CoTeTo.ebc_jsonld_files.mapping_jsonld import context_mapping
from CoTeTo.ebc_jsonld_files.mapping_jsonld import doc_mapping_brick
from CoTeTo.ebc_jsonld_files.budokeys_jsonld import context_keys
from CoTeTo.ebc_jsonld_files.budokeys_jsonld import doc_keys
from CoTeTo.ebc_jsonld_files.mapping_jsonld import doc_mapping_BUDO
from CoTeTo.ebc_jsonld_files.result_plot_setup_jsonld import context_plot_result
from CoTeTo.ebc_jsonld_files.result_plot_setup_jsonld import doc_plot_result

#When using this script alone

#from ebc_sql import EbcSql 
#from ebc_jsonld_files.initial_jsonld import context
#from ebc_jsonld_files.initial_jsonld import doc
#from ebc_jsonld_files.mapping_jsonld import context_mapping
#from ebc_jsonld_files.mapping_jsonld import doc_mapping_brick
#from ebc_jsonld_files.budokeys_jsonld import context_keys
#from ebc_jsonld_files.budokeys_jsonld import doc_keys
#from ebc_jsonld_files.mapping_jsonld import doc_mapping_BUDO
#from ebc_jsonld_files.result_plot_setup_jsonld import context_plot_result
#from ebc_jsonld_files.result_plot_setup_jsonld import doc_plot_result

 # Initialize a graph
RDFS # predefined namespace as 'http://www.w3.org/2000/01/rdf-schema#'
RDF # predefined namespace as 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
BRICK = Namespace('https://brickschema.org/schema/1.0.3/Brick#')
BF = Namespace('https://brickschema.org/schema/1.0.3/BrickFrame#')
EX = Namespace('http://example.com#')
BUDO=Namespace('https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#')  
   

###--------------------TOOL BouGen---------------------------------------------------###

outputpath='C:/Users/Juan/sciebo/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo'

def generate_boundary_condition_file(jsonldfile, outputpath):
# reading data from SQL database and writing them into mat File according to user requirements in jsonld
 
    
    data_jsonld = jsonld.compact(doc, {"@context": context})
    
    time_start = data_jsonld['TimeStart']
    time_end=data_jsonld['TimeEnd']
    for element in iter(data_jsonld['BUDOKey']['itemListElement']):
        key=str(element['BUDOBuildingAssignment'])+ '_' + str(element['BUDOSystem']) +  '_' +  str(element['BUDOSubsystem'])
        itemID=int(element['itemID'])
        (value_mea,time_mea,time_mea_date_form)=load_mea_result(key,itemID,time_start,time_end) 
        value_mea=convert_value(float(element['plus']),float(element['multiply']),value_mea)          
        matrix_name='data' 
        matrix=np.column_stack([value_mea.index, value_mea])
        output='/'.join(outputpath.split(".")[0].split('/')[0:-1])+'/'+str(element['itemID'])+'.mat'
        sci.io.savemat(output,{matrix_name:matrix}) 
            

def convert_value (plus,multiply,value):
#altering units of data
    if plus!="nan":
        value=value+float(plus)
    if multiply!="nan":
        value=value*float(multiply)
    return value


def load_mea_result(budo_key,itemID,time_start,time_end):
#loading measured data from databases
    path_to_config = os.path.join(os.path.dirname(os.path.realpath('__file__')),"res/settings_standard.ini")
    option_groups = "odbc_from"
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



###--------------------END OF TOOL BouGen---------------------------------------------------###
    

###--------------------TOOL BuToOn----------------------------------------------------------###

def budo_to_graph(jsonldfile):
 # Combine all functions in loops to read BUDO Keys from Excel file and generate BrickModel
    #from initial_jsonld import context
    #from initial_jsonld import doc

    data_jsonld = jsonld.compact(doc, {"@context": context})
    
   
    g = Graph()
    g.bind('ex', EX)
    g.bind('brick', BRICK)
    g.bind('bf', BF)
    g.bind('rdfs', RDFS)
    g.bind('rdf', RDF)
    g.bind('budo', BUDO)
    
    (brick_dict,budo_dict)=generate_brick_budo_dic() 
    
    zone = data_jsonld['Zone']  
        
    points=[]
    for element in iter(data_jsonld['BUDOConnection']['itemListElement']): 
        if str(element['ConnectionType']['@type'])=='hasPoint':
            points.append(str(element['Point']['BUDOSubsystem']).split('-')[1])

    equipments=[] 
    for element in iter(data_jsonld['BUDOConnection']['itemListElement']): 
        if str(element['ConnectionType']['@type'])=='hasPoint' and str(element['Equipment']['BUDOSubsystem']).split('-')[-1] not in equipments:
            equipments.append(element['Equipment']['BUDOSubsystem'].split('-')[-1])
        elif str(element['ConnectionType']['@type'])=='feeds':
            if 'portHeatflow.prim_1' in element and str(element['portHeatflow.prim_1']['BUDOSubsystem']).split('-')[-1] not in equipments:
                equipments.append(str(element['portHeatflow.prim_1']['BUDOSubsystem']).split('-')[-1])
            
            elif 'portHeatflow.prim_2' in element and str(element['portHeatflow.prim_2']['BUDOSubsystem']).split('-')[-1] not in equipments:
                equipments.append(element['portHeatflow.prim_2']['BUDOSubsystem'].split('-')[-1])
            
            elif 'portHeatflow.sec_1' in element and str(element['portHeatflow.sec_1']['BUDOSubsystem']).split('-')[-1] not in equipments:
                equipments.append(element['portHeatflow.sec_1']['BUDOSubsystem'].split('-')[-1])
            
            elif 'portHeatflow.sec_2' in element and str(element['portHeatflow.sec_2']['BUDOSubsystem']).split('-')[-1] not in equipments:
                equipments.append(element['portHeatflow.sec_2']['BUDOSubsystem'].split('-')[-1])

     
    points_dic={}
    equipments_dic={}
    data={'BUDO':[], 'explanation':[],'parameter':[], 'tag':[], 'unit':[],'value':[]}
    
   
    jsonld_BUDOS = jsonld.compact(doc_keys, {"@context": context_keys})


    systems=[*jsonld_BUDOS['itemListElement']]


    list_elements=[]

    for system in systems:
        for element in jsonld_BUDOS['itemListElement'][str(system)]['itemListElement']:  
            list_elements.append([element['BUDOKey'], element['itemID'], str(system)])
            
    pt = pd.DataFrame(list_elements, columns = ['BUDO Key','Item ID', 'System'])    
    
    for row in pt.iterrows():
        budo_split=str(row[1][0]).split('_')
        if budo_split[2].split('-')[1] == zone and  len(budo_split[3].split('-'))>1:
           if budo_split[3].split('-')[1] in points:
                point=budo_split[3].split('-')[1]
                instance=str(row[1][0])
                points_dic[point]=instance
                key=budo_split[-2].split('.')[0]
                if key in brick_dict.keys():
                    tag=brick_dict[key]
                elif key=='MEA':
                    key=budo_split[-2]
                    tag=brick_dict[key]
                g.add((EX[instance], RDF.type,  BRICK[tag]))
                g.add((EX[instance], BUDO['itemID'],Literal(str(row[1][1]))))
                data=create_data_property_dataframe(points_dic[point],tag,data)
           elif budo_split[3].split('-')[1] in equipments:
               equipment=budo_split[3].split('-')[1]
               if budo_split[-1] in["AI","AO","BI","BO"]:
                    instance=str(row[1][0])
                    key=budo_split[3].split('-')[0].split('.')[0]
                    if equipment not in equipments_dic.keys():
                        equipments_dic[equipment]='_'.join(budo_split[0:-2])                                      
                        if key in brick_dict.keys():
                            tag=brick_dict[key]
                        else:
                            key=budo_split[2].split('-')[0].split('.')[0]
                            tag=brick_dict[key]
                        g.add((EX[equipments_dic[equipment]], RDF.type, BRICK[tag]))
                        g=add_port(equipments_dic[equipment],tag,g)
                        data=create_data_property_dataframe(equipments_dic[equipment],tag,data)
                    key=budo_split[-2].split('.')[0]
                    tag=brick_dict[key]
                    g.add((EX[instance], RDF.type,  BRICK[tag]))
                    g.add((EX[instance], BUDO['itemID'],Literal(str(row[1][1]))))
                    g.add((EX[equipments_dic[equipment]], BF.hasPoint, EX[instance])) 
               else:
                    equipments_dic[equipment]=str(row[1][0])
                    key=budo_split[3].split('-')[0].split('.')[0]
                    if key in brick_dict.keys():
                        tag=brick_dict[key]
                        g.add((EX[equipments_dic[equipment]], RDF.type, BRICK[tag]))
                    elif key in budo_dict.keys():
                        tag=budo_dict[key]
                        g.add((EX[equipments_dic[equipment]], RDF.type, BUDO[tag]))
                    else:
                        key=budo_split[2].split('-')[0].split('.')[0]
                        tag=brick_dict[key]
                        g.add((EX[equipments_dic[equipment]], RDF.type, BRICK[tag]))
                    g=add_port(equipments_dic[equipment],tag,g)
                    data=create_data_property_dataframe(equipments_dic[equipment],tag,data)
#    print(equipments_dic)
#    print(points_dic)    
    connect_dic=generate_connect_dic()
#    print(connect_dic)
    g=add_relationship(g,connect_dic,equipments_dic,points_dic)    
    data=add_boundary_condition_to_dataframe(g,data)
    dataframe=delete_repeated_medium_property(data,g)
    return g,dataframe              
               
               
              
               
def generate_brick_budo_dic():
#reading mapping rules of BUDO Keys to Brick Schema and BUDO-M ontologies, and storing them in dictionaries
    
    #Importing data from jsonld file written in a python script named "initial_jsonld.py":

    #from initial_jsonld import context
    #from initial_jsonld import doc

    data_jsonld = jsonld.compact(doc, {"@context": context}) 
    
    brick_dict_swipe=data_jsonld['BUDONames']['itemListElement'][0]
    brick_dict = {val:key for (key, val) in brick_dict_swipe.items()}
    budo_dict_swipe=data_jsonld['BUDONames']['itemListElement'][1]
    budo_dict = {val:key for (key, val) in budo_dict_swipe.items()}
    
    return brick_dict,budo_dict
    
def generate_connect_dic():
#reading connections between components and storing them in dictionary
    #from initial_jsonld import context
    #from initial_jsonld import doc

    data_jsonld = jsonld.compact(doc, {"@context": context}) 
    
    connect_dic={'PRIM_PRIM':[],
                     'SEC_PRIM':[],
                     'PRIM_SEC':[],
                     'SEC_SEC':[],
                     'hasPoint':[]}
    
          
    for element in iter(data_jsonld['BUDOConnection']['itemListElement']): 
        if str(element['ConnectionType']['@type'])=='hasPoint':            
            pair=[str(element['Equipment']['BUDOSubsystem']).split('-')[-1], str(element['Point']['BUDOSubsystem']).split('-')[-1]]
            connect_dic['hasPoint'].append(pair)
        elif str(element['ConnectionType']['@type'])=='feeds':
            if 'portHeatflow.prim_1' in element and 'portHeatflow.prim_2' in element:
                pair=[str(element['portHeatflow.prim_1']['BUDOSubsystem']).split('-')[-1], str(element['portHeatflow.prim_2']['BUDOSubsystem']).split('-')[-1]]
                connect_dic['PRIM_PRIM'].append(pair)
            elif 'portHeatflow.sec_1' in element and 'portHeatflow.sec_2' in element:
                pair=[str(element['portHeatflow.sec_1']['BUDOSubsystem']).split('-')[-1], str(element['portHeatflow.sec_2']['BUDOSubsystem']).split('-')[-1]]
                connect_dic['SEC_SEC'].append(pair)
            elif 'portHeatflow.prim_1' in element and 'portHeatflow.sec_2' in element:
                pair=[str(element['portHeatflow.prim_1']['BUDOSubsystem']).split('-')[-1], str(element['portHeatflow.sec_2']['BUDOSubsystem']).split('-')[-1]]
                connect_dic['PRIM_SEC'].append(pair)
            elif 'portHeatflow.sec_1' in element and 'portHeatflow.prim_1' in element:
                pair=[str(element['portHeatflow.sec_1']['BUDOSubsystem']).split('-')[-1], str(element['portHeatflow.prim_2']['BUDOSubsystem']).split('-')[-1]]
                connect_dic['SEC_PRIM'].append(pair)
       
    return connect_dic             
    
def add_port(instance,tag,g):
#adding port to components
    if ('MX' in instance or 'DIV' in instance)or 'Heat_Pump' in tag or 'Heat_Exchanger'in tag:
        g.add((EX[instance+'_PH.PRIM'], RDF.type, BUDO['portHeatflow.prim']))
        g.add((EX[instance], BF.hasPart, EX[instance+'_PH.PRIM']))
        g.add(( EX[instance+'_PH.SEC'], RDF.type, BUDO['portHeatflow.sec']))
        g.add((EX[instance], BF.hasPart, EX[instance+'_PH.SEC']))
    else:
        g.add(( EX[instance+'_PH'], RDF.type, BUDO['portHeatflow']))
        g.add((EX[instance], BF.hasPart,  EX[instance+'_PH']))
    if 'DIV' in instance:
        g.add(( EX[instance+'_PH.SEC'], BF.isFedBy, EX[instance+'_PH.PRIM']))  
    if 'MX' in instance: 
        g.add(( EX[instance+'_PH.SEC'], BF.feeds, EX[instance+'_PH.PRIM']))  
    return g


def create_mapping_dict():
    
    mapping_brick_jsonld = jsonld.compact(doc_mapping_brick, {"@context": context_mapping})
    
    systems_mapping_brick=[]    
    for element in mapping_brick_jsonld['itemListElement']:
        systems_mapping_brick.append(*element)
        
  
    list_elements_for_data_frame=[]    
    for element in mapping_brick_jsonld['itemListElement']:            
        list_elements_for_data_frame.append(next(iter(element.values())))
        
    list_elements_for_data_frame2=[]         
    for element in list_elements_for_data_frame:
        list_elements_for_data_frame2.append([element['Point'], element['BUDOSystem'], element['ModelicaModel'], element['portHeatflow'], element['EquipmentPointParameter'], element['EquipmentPointUnits'], element['EquipmentPointExplanation'], element['portParameter'], element['portUnits'], element['portExplanation']])

					
    df_brick = pd.DataFrame(list_elements_for_data_frame2, columns = ['Point','BUDOSystem', 'ModelicaModel', 'portHeatflow', 'EquipmentPointParameter', 'EquipmentPointUnits', 'EquipmentPointExplanation', 'portParameter', 'portUnits', 'portExplanation'])    
    df_brick['Equipment'] = systems_mapping_brick
    cols_brick=['Equipment','Point','BUDOSystem', 'ModelicaModel', 'portHeatflow', 'EquipmentPointParameter', 'EquipmentPointUnits', 'EquipmentPointExplanation', 'portParameter', 'portUnits', 'portExplanation']
    df_brick=df_brick[cols_brick]
    df_brick['ModelicaModel']=df_brick['ModelicaModel'].astype(int)
    df_brick['portHeatflow']=df_brick['portHeatflow'].astype(int)
    
       
    mapping_BUDO_jsonld = jsonld.compact(doc_mapping_BUDO, {"@context": context_mapping})
    
    systems_mapping_BUDO=[]    
    for element in mapping_BUDO_jsonld['itemListElement']:
        if len(mapping_BUDO_jsonld['itemListElement'])==1:
            systems_mapping_BUDO.append(element)
        else:
            systems_mapping_BUDO.append(*element)
 
        
  
    list_elements_for_data_frame_BUDO=[]
    if len(mapping_BUDO_jsonld['itemListElement'])==1:
        list_elements_for_data_frame_BUDO.append(mapping_BUDO_jsonld['itemListElement'][systems_mapping_BUDO[0]])
    else:
        for element in mapping_BUDO_jsonld['itemListElement']:            
            list_elements_for_data_frame_BUDO.append(next(iter(element.values())))
        
    list_elements_for_data_frame2_BUDO=[]         
    for element in list_elements_for_data_frame_BUDO:
        list_elements_for_data_frame2_BUDO.append([element['Point'], element['BUDOSystem'], element['ModelicaModel'], element['portHeatflow'], element['EquipmentPointParameter'], element['EquipmentPointUnits'], element['EquipmentPointExplanation'], element['portParameter'], element['portUnits'], element['portExplanation']])

					
    df_BUDO = pd.DataFrame(list_elements_for_data_frame2_BUDO, columns = ['Point','BUDOSystem', 'ModelicaModel', 'portHeatflow', 'EquipmentPointParameter', 'EquipmentPointUnits', 'EquipmentPointExplanation', 'portParameter', 'portUnits', 'portExplanation'])    
    df_BUDO['Equipment'] = systems_mapping_BUDO
    cols_BUDO=['Equipment','Point','BUDOSystem', 'ModelicaModel', 'portHeatflow', 'EquipmentPointParameter', 'EquipmentPointUnits', 'EquipmentPointExplanation', 'portParameter', 'portUnits', 'portExplanation']
    df_BUDO=df_BUDO[cols_BUDO]
    df_BUDO['ModelicaModel']=df_BUDO['ModelicaModel'].astype(int)
    df_BUDO['portHeatflow']=df_BUDO['portHeatflow'].astype(int)
    
    df_brick = df_brick.replace(r'^\s*$', np.nan, regex=True)
    df_BUDO = df_BUDO.replace(r'^\s*$', np.nan, regex=True)

 
    dict_mapping={"BRICK": df_brick, "BUDO": df_BUDO}
    

    return dict_mapping






               
def create_data_property_dataframe(instance,tag,data):
    
    
#generating dataproperties for components and storing them in dataframe
    gf = Graph()
    gf.bind('brick', BRICK)
    gf.bind('ex', EX)
    gf.bind('budo', BUDO) 
    gf.parse(os.path.join(os.path.dirname(os.path.realpath('__file__')),'Loaders/Auxiliary/BRICK/Brick.ttl'), format='turtle')
    gf.parse(os.path.join(os.path.dirname(os.path.realpath('__file__')),'Loaders/Auxiliary/BUDO_M/BUDO-M.ttl'), format='turtle')
    
    
    ports_ontology=['portHeatflow.prim','portHeatflow.sec','portHeatflow.ter']
    ports_budokey=['PH.PRIM','PH.SEC','PH.TER']
    
    dict_mapping=create_mapping_dict()
    
    for ontology in dict_mapping:
        pt=dict_mapping[ontology]  
        for row in pt.iterrows():
            classes=str(row[1][0])
            if ontology=="BRICK":
                res=gf.query("""ASK{brick:%s rdfs:subClassOf*  brick:%s }""" %(tag,classes))
            else:
                res=gf.query("""ASK{budo:%s rdfs:subClassOf*  budo:%s }""" %(tag,classes))
            if res:
                if str(row[1][5])!='nan':
                    data_property=str(row[1][5]).split('/')
                    data_unit=str(row[1][6]).split(',')
                    data_explanation=str(row[1][7]).split('/')
                    for (properties,units,explanations) in zip(data_property,data_unit,data_explanation):
                        data['tag'].append(tag)
                        data['BUDO'].append(instance)
                        data['parameter'].append(properties)
                        data['value'].append("None")
                        data['unit'].append(units)
                        data['explanation'].append(explanations)
                for i in range (0,row[1][4]):
                    if classes=='Valve'and (not('DIV' in instance or 'MX' in instance)):
                        break
                    if str(row[1][8])!='nan':
                        if row[1][4]==1:
                            port_tag='portHeatflow'
                            port_key='PH'
                        else:
                            port_tag=ports_ontology[i]
                            port_key=ports_budokey[i]
                        port_data_property=str(row[1][8]).split('/')
                        port_data_unit=str(row[1][9]).split(',')
                        port_data_explanation=str(row[1][10]).split('/')
                        for (properties,units,explanations) in zip(port_data_property,port_data_unit,port_data_explanation):      
                            data['tag'].append( port_tag)
                            data['BUDO'].append(instance+'_'+port_key)
                            data['parameter'].append(properties)
                            data['value'].append("None")
                            data['unit'].append(units)
                            data['explanation'].append(explanations)
    return data

def delete_repeated_medium_property(data,g):
#deleting repeated declaration of data property medium in one fluid system
    df = pd.DataFrame(data)
    medium_list=[]
    drop_list=[]
    for index, row in df.iterrows():
        if row["parameter"]=='medium':
            medium_repeated=check_medium_property_repeatation(g,row["tag"],medium_list,row["BUDO"])
            if medium_repeated:
               drop_list.append(index)
            else:
                medium_list.append(row["BUDO"])
    df_final=df.drop(drop_list)
    return df_final    
        
    
def check_medium_property_repeatation(g,tag,medium_list,instance): 
#finding repeated declaration of data property medium in one fluid system
    if "portHeatflow" in tag:
        rows=g.query( """SELECT ?o WHERE{  { ex:%s bf:feeds*  ?o.}union{  ex:%s bf:isFedBy* ?o.}union {{  ex:%s bf:feeds*  ?e.}union{  ex:%s bf:isFedBy* ?e.} ?e bf:hasPoint ?o.}} """ %(instance,instance,instance,instance))
    else:
        rows=g.query( """SELECT ?o WHERE{ ex:%s bf:isPointOf ?a.  {?a bf:feeds*  ?o.}union{ ?a bf:isFedBy* ?o.}union {{ ?a bf:feeds*  ?e.}union{ ?a bf:isFedBy* ?e.} ?e bf:hasPoint ?o.}} """ %(instance))
    m = {'http://example.com':''}
    res = [[m[r.split('#')[0]]+ r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
    medium_repeated=False
    for row in res:        
        if row[0] in medium_list:
            medium_repeated=True 
    return medium_repeated


def add_boundary_condition_to_dataframe(g,data): 
# finding our boundaries of systems, adding boundary data properties into dataframe
    rows = g.query("""SELECT ?s WHERE {?m bf:hasPart ?s. MINUS {?s bf:isFedBy ?n.}}""")
    m = {'http://example.com':'',}
    res = [[m[r.split('#')[0]]+ r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows] 
    ports_dict={'PH.PRIM':'portHeatflow.prim','PH.SEC':'portHeatflow.sec','PH.TER':'portHeatflow.ter','PH':'portHeatflow'}
    for equipment in res: 
         for item in equipment:
             for properties,explanations,units in zip(['boundarypath.temperature','boundarypath.massflow'],['mat file directory for boundary condition temperature when needed','mat file directory for boundary condition massflow when needed'],['K','kg/s']):
                data['tag'].append(ports_dict[item.split('_')[-1]])
                data['BUDO'].append(item)
                data['parameter'].append(properties)
                data['value'].append("None")
                data['unit'].append(units)
                data['explanation'].append(explanations)
    return data           
                             

    
def add_data_property_excelsheet(dataframe,sheet_name,path): 
#writing content of data property dataframe into a new worksheet of an Excel file
    writer = StyleFrame.ExcelWriter(path)    
    book = load_workbook(writer.path)
    writer.book = book
    sf = StyleFrame(dataframe)
    sf.set_column_width(columns=['tag', 'BUDO','parameter','explanation','value'], width=60)
    sf.to_excel(writer,sheet_name)
    writer.save()
    writer.close()
 

   
def add_relationship(g,connect_dic,equipments_dic,points_dic):
#Adding relationship between components
    for relationship in connect_dic.keys():
        if relationship=="hasPoint":
           for item in connect_dic[relationship]:
               if (len(equipments_dic[item[0]].split("_"))==4 and (equipments_dic[item[0]].split("_")[2].split('-')[0].split('.')[0] in ['HP','HX'])) or 'DIV' in equipments_dic[item[0]] or 'MX' in equipments_dic[item[0]] :#BUDO                  
                   if  'HP' in equipments_dic[item[0]] and "WS.H" in points_dic[item[1]]:
                       g.add((EX[equipments_dic[item[0]]+'_PH.PRIM'], BF["hasPoint"], EX[points_dic[item[1]]]))
                   if  'HP' in equipments_dic[item[0]] and "WS.CH" in points_dic[item[1]]:
                       g.add((EX[equipments_dic[item[0]]+'_PH.SEC'], BF["hasPoint"], EX[points_dic[item[1]]])) 
                   if  ('HX' in equipments_dic[item[0]] or  'DIV' in equipments_dic[item[0]] or 'MX' in equipments_dic[item[0]])and "PRIM" in points_dic[item[1]]:
                       g.add((EX[equipments_dic[item[0]]+'_PH.PRIM'], BF["hasPoint"], EX[points_dic[item[1]]]))
                   if  ('HX' in equipments_dic[item[0]] or  'DIV' in equipments_dic[item[0]] or 'MX' in equipments_dic[item[0]]) and "SEC" in points_dic[item[1]]:
                       g.add((EX[equipments_dic[item[0]]+'_PH.SEC'], BF["hasPoint"], EX[points_dic[item[1]]]))
               else:                   
                   g.add((EX[equipments_dic[item[0]]+'_PH'], BF["hasPoint"], EX[points_dic[item[1]]]))
        else:
            for item in connect_dic[relationship]:
                relate=relationship.split('_')
                if (len(equipments_dic[item[0]].split("_"))==4 and ('HX' in equipments_dic[item[0]] or 'HP' in equipments_dic[item[0]])) or 'DIV' in equipments_dic[item[0]] or 'MX' in equipments_dic[item[0]]:
                    port_out=equipments_dic[item[0]]+'_PH.'+relate[0]
                else:
                    port_out=equipments_dic[item[0]]+'_PH'
                if (len(equipments_dic[item[1]].split("_"))==4 and ('HX' in equipments_dic[item[1]] or 'HP' in equipments_dic[item[1]])) or 'DIV' in equipments_dic[item[1]] or 'MX' in equipments_dic[item[1]]:
                    port_in=equipments_dic[item[1]]+'_PH.'+relate[1]
                else:
                    port_in=equipments_dic[item[1]]+'_PH'                  
                g.add((EX[port_out], BF["feeds"], EX[port_in]))
    g=add_reverse_relationship(g)
    return g


def add_reverse_relationship(g):
#Adding reverse relationships between components
    res = g.query("SELECT ?a ?b WHERE { ?a bf:hasPart ?b .}")
    for row in res:
        g.add((row[1], BF.isPartOf, row[0]))
    res = g.query("SELECT ?a ?b WHERE { ?a bf:isPartOf ?b .}")
    for row in res:
        g.add((row[1], BF.hasPart, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:hasPoint ?b .}")
    for row in res:
        g.add((row[1], BF.isPointOf, row[0]))
    res = g.query("SELECT ?a ?b WHERE {?a bf:isPointOf ?b .}")
    for row in res:
        g.add((row[1], BF.hasPoint, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:feeds ?b .}")
    for row in res:
        if '_'.join(row[1].split('_')[0:-1])!='_'.join(row[0].split('_')[0:-1]):
            g.add((row[1], BF.isFedBy, row[0]))
    res = g.query("SELECT ?a ?b WHERE {?a bf:isFedBy ?b .}")
    for row in res:
        if '_'.join(row[1].split('_')[0:-1])!='_'.join(row[0].split('_')[0:-1]):
            g.add((row[1], BF.feeds, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:contains ?b .}")
    for row in res:
        g.add((row[1], BF.isLocatedIn, row[0]))
    res = g.query("SELECT ?a ?b WHERE {?a bf:isLocatedIn ?b .}")
    for row in res:
        g.add((row[1], BF.contains, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:controls ?b .}")
    for row in res:
        g.add((row[1], BF.isControlledBy, row[0]))
    res = g.query("SELECT ?a ?b WHERE {?a bf:isControlledBy ?b .}")
    for row in res:
        g.add((row[1], BF.controls, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:hasOutput ?b .}")
    for row in res:
        g.add((row[1], BF.isOutputOf, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:hasInput ?b .}")
    for row in res:
        g.add((row[1], BF.isInputOf, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:hasTagSet ?b .}")
    for row in res:
        g.add((row[1], BF.isTagSetOf, row[0]))
    
    res = g.query("SELECT ?a ?b WHERE {?a bf:hasToken ?b .}")
    for row in res:
        g.add((row[1], BF.isTokenOf, row[0]))
    
    return g



    #-----OnWithData. Now implemented inside BuToOn
    

def read_data_property_edited(g,data_property):
#reading data properties values from edited data property file data frame file and combine them into BrickModel with Data Property relationship
    
    for row in data_property.iterrows():
        if str(row[1][5])!="None":            
            g.add((EX[str(row[1][0])], BUDO[str(row[1][2])],  Literal(str(row[1][5]))))
    return g


#---------------END OF TOOL BuToOn-----------------------
    
#--------------------OnToMo------------------------------



def get_points(class_name,g,ontology,u):   
#SPARQL queries for finding out instance belonging to given classes   
    
    

    g.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)),'Loaders/Auxiliary/BRICK/Brick.ttl'), format='turtle')
    g.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)),'Loaders/Auxiliary/BUDO_M/BUDO-M.ttl'), format='turtle')
    if ontology=="BRICK":
        rows = g.query("""
        SELECT ?s
        WHERE {
            ?p rdf:type owl:Class.
            ?p rdfs:subClassOf* brick:%s .
            ?s rdf:type ?p .
           
        }
        """ %(class_name))
    else:
        rows = g.query("""
        SELECT ?s
        WHERE {
            ?p rdf:type owl:Class.
            ?p rdfs:subClassOf* budo:%s .
            ?s rdf:type ?p .
        }
        """ %(class_name)) 
    m = {
        'https://brickschema.org/schema/1.0.3/Brick': 'brick',
        'http://www.w3.org/1999/02/22-rdf-syntax-ns': 'rdf',
        'http://www.w3.org/2000/01/rdf-schema': 'rdfs',
        'https://brickschema.org/schema/1.0.3/BrickFrame': 'bf',
        'http://www.w3.org/2002/07/owl': 'owl',
        'http://www.w3.org/2004/02/skos/core': 'skos',
        'http://example.com': '',
        'https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#':'budo'
        }
    res = [[m[r.split('#')[0]] + r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
    return res

def ask_if_model_with_pipe():
#ask user choices, if generating model with pipe lines
    root = tkinter.Tk()
    root.title("")
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (250, 150, (screenwidth - 250)/2, (screenheight - 150)/2)
    root.geometry(size)    
    group = tkinter.LabelFrame(root,text = 'Generate model with pipeline?',padx = 5,pady = 5)
    group.pack(padx = 10,pady = 10)
    options = ['Yes','No']
    v = tkinter.StringVar()
    v.set('Yes')
    for choice in options:
        tkinter.Radiobutton(group,text =choice,variable = v,value = choice).pack(anchor = tkinter.W)
    tkinter.Button(root, text ="confirm",command=root.destroy).pack()
    root.mainloop()
    choice=v.get()    
    return choice                      
                     


#--------------------END OF OnToMo------------------------------
    
#-----------------------ResPlot--------------------------------
    
def plot_sim_graph(simrespath):
#print the graph of simulationsresult and measured data
    
    #Changes
    
    data_jsonld = jsonld.compact(doc, {"@context": context})
    
    time_start = data_jsonld['TimeStart']
    time_end=data_jsonld['TimeEnd']
    
    jsonld_plot_result = jsonld.compact(doc_plot_result, {"@context": context_plot_result})

    list_elements_BUDOKey_joined=[]
    
    for element in jsonld_plot_result['ResultsToPlot']['itemListElement']:
        list_elements_BUDOKey_joined.append([element['ModelicaModel'], str(element['BUDOKey']['BUDOBuildingAssignment']) + '_._' + str(element['BUDOKey']['BUDOSystem']) + '_' + str(element['BUDOKey']['BUDOSubsystem']) + '_' + str(element['BUDOKey']['BUDOPositionMedium']) + '_' + str(element['BUDOKey']['BUDOType']) + '_' + str(element['BUDOKey']['BUDOIOFunction']) , element['itemID'], element['plus'], element['multiply']])
        
     
         
    pt = pd.DataFrame(list_elements_BUDOKey_joined, columns = ['ModelicaModel', 'BUDO Key','Item ID', 'Plus', 'Multiply'])    
    
    
    #end changes
    
    
    
    for row in pt.iterrows():
        if str(row[1][1])!="nan":
            sns.set_palette("muted")
            sns.set_style("whitegrid")
            key='_'.join(str(row[1][1]).split('_')[0:4])
            itemID=int(row[1][2])
            (value_mea,time_mea,time_mea_date_form)=load_mea_result(key,itemID,time_start,time_end)  
            value_mea=convert_value(str(row[1][3]),str(row[1][4]),value_mea)
            if  str(row[1][0])=="nan": 
                plt.plot(time_mea_date_form, value_mea, label=str(row[1][1]))                               
            else: 
                variable=str(row[1][0])  
                value_sim,time_sim=load_sim_result(simrespath,variable)
#                value_mea=reshape_mea_result(value_mea,time_mea,time_sim)
                plt.plot(time_mea, value_mea, label=str(row[1][1]))
                plt.plot(time_sim, value_sim, label=str(row[1][1])+'_SIM')
            axes=plt.gca()
            #            axes.set_ylim([0, 40])
            for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(20) 
            for tick in axes.yaxis.get_major_ticks():
                tick.label.set_fontsize(20)     
            for tick in axes.get_xticklabels():
                tick.set_rotation(0)
            axes.legend(prop={'size': 20})
            plt.xlabel("time (in s)", fontsize = 32)
            plt.ylabel("temperature (in °C)", fontsize = 32)            
            font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 35}            
            mpl.rc('font', **font)
            fig=plt.gcf()
            fig.set_size_inches(18.5, 10.5, forward=True)
            plt.show()
            if  str(row[1][0])!="nan":       
                plt.figure()
#            fig.savefig('simulation_results.png', dpi=fig.dpi, bbox_inches='tight')     
                

def load_sim_result(simrespath,variable):
#loading simulation results
    sims, __ = modelicares.load(simrespath)
    value_sim = sims[variable].values()
    time_sim=sims[variable].times()
    value_sim=value_sim[0]
    time_sim=time_sim[0]
    return value_sim,time_sim

def reshape_mea_result(value_mea,time_mea,time_sim):
#interploting measured data in order to have the same scope with the simulated data.
    tck =sci.interpolate.splrep(time_mea, value_mea)
    value_mea = sci.interpolate.splev(time_sim,tck)
    return value_mea
              

def RMSE(value_mea,value_sim):
    """root mean square error"""
    rmse=np.sqrt(((value_mea-value_sim) ** 2).mean())
    return rmse

def MAE(value_mea,value_sim):
    """mean absolute error"""
    mea=abs(value_mea-value_sim).mean()
    return mea

def NRMSE(value_mea,value_sim):
    """normalized root mean square error """
    nrmse=RMSE(value_mea,value_sim)/(value_mea.max()-value_mea.min())
    return nrmse

def analyse_result(simrespath):
#output MAE,RMSE and NRMSE metrics of simulation result and measured data
    
    data_jsonld = jsonld.compact(doc, {"@context": context})
    
    time_start = data_jsonld['TimeStart']
    time_end=data_jsonld['TimeEnd']
    
    jsonld_plot_result = jsonld.compact(doc_plot_result, {"@context": context_plot_result})

    list_elements_BUDOKey_joined=[]
    
    for element in jsonld_plot_result['ResultsToPlot']['itemListElement']:
        list_elements_BUDOKey_joined.append([element['ModelicaModel'], str(element['BUDOKey']['BUDOBuildingAssignment']) + '_._' + str(element['BUDOKey']['BUDOSystem']) + '_' + str(element['BUDOKey']['BUDOSubsystem']) + '_' + str(element['BUDOKey']['BUDOPositionMedium']) + '_' + str(element['BUDOKey']['BUDOType']) + '_' + str(element['BUDOKey']['BUDOIOFunction']) , element['itemID'], element['plus'], element['multiply']])
        
     
         
    pt = pd.DataFrame(list_elements_BUDOKey_joined, columns = ['ModelicaModel', 'BUDO Key','Item ID', 'Plus', 'Multiply'])    
    
    
    
    result={"budo key":[],"MAE":[],"RMSE":[],"NRMSE":[]}
    for row in pt.iterrows():
        if str(row[1][1])!="nan":
            key='_'.join(str(row[1][1]).split('_')[0:4])
            itemID=int(row[1][2])
            (value_mea,time_mea,time_mea_date_form)=load_mea_result(key,itemID,time_start,time_end)
            variable=str(row[1][0])  
            (value_sim,time_sim)=load_sim_result(simrespath,variable)
            value_mea=reshape_mea_result(value_mea,time_mea,time_sim)
            value_mea=convert_value(str(row[1][3]),str(row[1][4]),value_mea) 
            rmse=RMSE(value_mea,value_sim)            
            mae=MAE(value_mea,value_sim)           
            nrmse=NRMSE(value_mea,value_sim)
            result["budo key"].append(str(row[1][1]))
            result["MAE"].append(mae)
            result["RMSE"].append(rmse)
            result["NRMSE"].append(nrmse)
            df_result = pd.DataFrame(result)
    print (df_result)
    return df_result


#--------------------END OF ResPlot------------------------------