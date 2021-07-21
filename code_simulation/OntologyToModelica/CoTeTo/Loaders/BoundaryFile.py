# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 20:21:23 2018

@author: Yingying Yang
"""

from CoTeTo.Loader import Loader
from os.path import isfile
from CoTeTo import jsonld_budo_to_ontology as bo   
    

class BoundaryFile(Loader):
    name = 'BoundaryFile'
    description = 'load requirements of timeseries data '
    version = '1.0'
    author = 'Yingying Yang, Belén Llopis'
    helptxt = """Loading InputDataProperty File with filled "setup" jsonld"""

    def load(self, uriList,outputBase):
        for u in uriList:
            if isfile(u):
                self.logger.info('BoundaryFile - loading %s', u)
                bo.generate_boundary_condition_file(u,outputBase)
            else:
                self.logger.error('BoundaryFile - file not readable %s', u) 

           