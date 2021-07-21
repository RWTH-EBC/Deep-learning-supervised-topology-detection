#-*- coding:utf-8 -*-
#
"""
Created on Fri Jun  8 03:31:41 2018

@author: Yingying Yang
"""
import os
from CoTeTo.Loader import Loader
from os.path import isfile
from rdflib import Graph
import pandas as pd
from pyld import jsonld
from collections import defaultdict
from CoTeTo import jsonld_budo_to_ontology as bo



class TurtleFile(Loader):
    name = 'TurtleFile'
    description = 'Turtle file loader'
    version = '1.0'
    author = 'Yingying Yang, Belén Llopis'
    helptxt = """Loading BrickModel in turtle format"""

    def load(self, uriList,outputBase):
        data = {}
        for u in uriList:
            if isfile(u):
                self.logger.info('TurtleFile - loading %s', u)
                content={}
                g = Graph()
                g.parse(u, format='turtle') 
                modelica_map={}
                modelica_additional_model_number={}
                
                dict_mapping=bo.create_mapping_dict()

                
                for ontology in dict_mapping:
                    pt=dict_mapping[ontology]
                    pd.set_option('max_colwidth',80)
                    Result = defaultdict(list)
                    for row in pt.iterrows():
                        modelica_map[str(row[1][2])]=str(row[1][0])       
                        acr=str(row[1][2]) #acronym in BUDO
                        tag=str(row[1][0]) #model in modelica
                        print ("Runing query for %s ......" %acr)
                        res = bo.get_points(tag,g,ontology,u)
                        print ("\tNumber of points found for %s : %d" % (tag,len(res)))
                        if len(res)!=0:
                            Result[acr].append(res)
                        if (row[1][3]!=0): #additional model Modelica different than 0
                            modelica_additional_model_number[str(row[1][2])]=int(row[1][3])
                        content[ontology]=Result
#                    name=os.path.split(u)[1]
#                    data[name]=Group
                content["modelica_map"]= modelica_map
                content["modelica_additional_model_number"]= modelica_additional_model_number
                content["outputfile_name"]=(outputBase.split(".")[-2]).split("/")[-1]
                content["pipe"]=bo.ask_if_model_with_pipe()
                data[u]=content
                print(data)
            else:
                data[u] = None
                self.logger.error('TurtleFile - file not readable %s', u)
        return data 
    
