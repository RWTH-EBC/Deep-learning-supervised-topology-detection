context_plot_result = {
        "schema": "http://www.w3.org/2001/XMLSchema#",
        "brick": "http://brickschema.org/schema/1.0.3/Brick#",
        "brickFrame": "http://brickschema.org/schema/1.0.3/BrickFrame#",
        "BUDO-M": "https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        
        
        "Point": {"@id": "brick: Point"},
        "BUDOKey": {"@id": "BUDO-M: BUDOKey"},
        "BUDOConnection": {"@id": "BUDO-M: BUDOConnection"},
        "BUDOBuildingAssignment": {"@id": "BUDO-M: BUDOBuildingAssignment"},
        "BUDOSystem": {"@id": "BUDO-M: BUDOSystem"},
        "BUDOSubsystem": {"@id": "BUDO-M: BUDOSubsystem"},
        "BUDOPositionMedium": {"@id": "BUDO-M: BUDOPositionMedium"},
        "BUDOType": {"@id": "BUDO-M: BUDOType"},
        "BUDOIOFunction": {"@id": "BUDO-M: BUDOIOFunction"},
        "itemID": {"@id": "BUDO-M: ItemID"},
        "Equipment": {"@id": "brick: Equipment"},
        "ItemList": {"@id":"schema:ItemList"},
        "itemListElement": {"@id":"schema:itemListElement"},
        "BUDONames":  {"@id":"BUDO-M:BUDONames"},
        "multiply": {"@id": "BUDO-M: multiply"},
        "plus": {"@id": "BUDO-M: plus"},
        "ResultsToPlot": {"@id": "BUDO-M: ResultsToPlot"},
        "ModelicaModel": {"@id": "BUDO-M: ModelicaModel"}
        
       
}


doc_plot_result= {
       "@context": context_plot_result,
       
       "ResultsToPlot": {
              
               "@type": "ItemList",
               "itemListElement": [
       {
        
       "ModelicaModel": "Temperature_Sensor4.T",
       
       "BUDOKey": {
               
               "BUDOBuildingAssignment": "BL-4120",
               "BUDOSystem": "HP-K12",
               "BUDOSubsystem": "SEN.T-B01",
               "BUDOPositionMedium": "WS.H.SUP.PRIM",
               "BUDOType": "MEA.T",
               "BUDOIOFunction": "AI"},      
              
       
      "itemID": "1025",
      "plus": "273.15",
      "multiply": "0"
      },
      
        
      {
        
       "ModelicaModel": "Temperature_Sensor1.T",
       
       "BUDOKey": {
               
               "BUDOBuildingAssignment": "BL-4120",
               "BUDOSystem": "HP-K12",
               "BUDOSubsystem": "SEN.T-B11",
               "BUDOPositionMedium": "WS.CH.SUP.PRIM",
               "BUDOType": "MEA.T",
               "BUDOIOFunction": "AI"},      
              
       
      "itemID": "1034",
      "plus": "273.15",
      "multiply": "0"
       }
    
      
     ] 
      
      }
      
      }
