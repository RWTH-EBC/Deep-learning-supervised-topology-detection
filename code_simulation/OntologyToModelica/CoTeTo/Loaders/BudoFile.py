#-*- coding:utf-8 -*-
#
"""
Created on Thu Aug 2 13:54:27 2018

@author: Yingying Yang
"""
from CoTeTo.Loader import Loader
from os.path import isfile
from CoTeTo import jsonld_budo_to_ontology as bo
import os 
try: 
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from CoTeTo.properties_tkinter import EditorApp

   
    

class BudoFile(Loader):
    name = 'BudoFile'
    description = 'Budo jsonld file loader'
    version = '1.0'
    author = 'Yingying Yang, Belén Llopis'
    helptxt = """Loading InputDataFile in jsonld format with filled "setup" and "BUDO Keys. Editing for setting values and paths of time series." """

    def load(self, uriList,outputBase):
        d={}
        for u in uriList:
            if isfile(u):
                self.logger.info('BudoFile - loading %s', u)
                (g,data)=bo.budo_to_graph(u)
                #path=outputBase.split(".")[0]+'.xlsx'
                #bo.create_data_property_excel(data,'data_property',path)
                path_brick=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Auxiliary/BRICK/Brick.ttl')
                path_budo=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Auxiliary/BUDO_M/BUDO-M.ttl') 
                d['path_brick']=path_brick
                d['path_budo']=path_budo  
                d['Graph']=g
                
                
                ##Data Property File GUI
                
                def main():
                    #   start
                    root = tk.Tk()
                    editor = EditorApp(root, data)
                    root.mainloop()  # until closes window

                    #   re-assign dataframe
                    new_df = editor.df

                    #print ("THIS IS THE NEW DATABASE:")
                    #print (new_df.to_string(index=False))
    
                    return new_df

                    if __name__ == '__main__':
                        main()
                        
                edited_df=main()
                
                g=bo.read_data_property_edited(g,edited_df)
                
                d['Graph']=g
    

            else:
                d= None
                self.logger.error('BudoFile - file not readable %s', u)
            return d
                
    
    
            
    
