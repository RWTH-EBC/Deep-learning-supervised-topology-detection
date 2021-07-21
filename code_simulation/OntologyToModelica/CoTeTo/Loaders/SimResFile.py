# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 20:21:23 2018

@author: Yingying Yang
"""

from CoTeTo.Loader import Loader
from os.path import isfile
from CoTeTo import jsonld_budo_to_ontology as bo   
    

class SimResFile(Loader):
    name = 'SimResFile'
    description = 'Simulation Result jsonld file loader'
    version = '1.0'
    author = 'Yingying Yang'
    helptxt = """Loading InputDataFile in jsonld format with filled "result plot" and "setup", get timeseries data of the real building according to the item ID and compare them with data in mat file containing simulation result."""

    def load(self, uriList,outputBase):
        simrespath=None
        for u in uriList:
            if isfile(u):
                self.logger.info('SimResFile - loading %s', u)
                if u.split(".")[-1]=='mat':
                    simrespath=u
                
        if simrespath==None:
            self.logger.error('SimsResFile - file not readable %s', u)
        else:                     
            bo.plot_sim_graph(simrespath)
        if simrespath!=None:
            bo.analyse_result(simrespath)