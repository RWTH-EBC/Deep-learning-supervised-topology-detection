####           HEAT PUMP WITH BOUNDARY CONDITION        #####

context = {
        "schema": "http://www.w3.org/2001/XMLSchema#",
        "brick": "http://brickschema.org/schema/1.0.3/Brick#",
        "brickFrame": "http://brickschema.org/schema/1.0.3/BrickFrame#",
        "BUDO-M": "https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        
        "Zone": {"@id": "brick: HVAC Zone"},
        "TimeStart": {"@id": "schema: StartDate"},
        "TimeEnd": {"@id": "schema: EndDate"},
        "Point": {"@id": "brick: Point"},
        "BUDOKey": {"@id": "BUDO-M: BUDOKey"},
        "BUDOConnection": {"@id": "BUDO-M: BUDOConnection"},
        "ConnectionType": {"@id": "BUDO-M: ConnectionType"},
        "BUDOBuildingAssignment": {"@id": "BUDO-M: BUDOBuildingAssignment"},
        "BUDOSystem": {"@id": "BUDO-M: BUDOSystem"},
        "BUDOSubsystem": {"@id": "BUDO-M: BUDOSubsystem"},
        "BUDOPositionMedium": {"@id": "BUDO-M: BUDOPositionMedium"},
        "BUDOType": {"@id": "BUDO-M: BUDOType"},
        "BUDOIOFunction": {"@id": "BUDO-M: BUDOIOFunction"},
        "itemID": {"@id": "BUDO-M: ItemID"},
        "multiply": {"@id": "BUDO-M: multiply"},
        "plus": {"@id": "BUDO-M: plus"},
        "Equipment": {"@id": "brick: Equipment"},
        "hasPoint": {"@id": "brickFrame: hasPoint"},  
        "ItemList": {"@id":"schema:ItemList"},
        "itemListElement": {"@id":"schema:itemListElement"},
        "Pump":  {"@id":"brick:Pump"},
        "Boiler":  {"@id":"brick:Boiler"},
        "Valve":  {"@id":"brick:Valve"},
        "Temperature_Sensor":  {"@id":"brick:Temperature_Sensor"},
        "Heat_Pump":  {"@id":"brick:Heat_Pump"},
        "Combined_Heat_Power":  {"@id":"brick:Combined_Heat_Power"},
        "Heat_Exchanger":  {"@id":"brick:Heat_Exchanger"},
        "Setpoint":  {"@id":"brick:Setpoint"},
        "Command":  {"@id":"brick:Command"},
        "Alarm":  {"@id":"brick:Alarm"},
        "Status":  {"@id":"brick:Status"},
        "T_Piece":  {"@id":"BUDO-M:T_Piece"},
        "BUDONames":  {"@id":"BUDO-M:BUDONames"}
        
       
}


doc = {
    
        "@context": context,
        "Zone":"K12",
        "TimeStart": "2015-01-01 00:00:00",
        "TimeEnd": "2015-01-08 00:00:00",
        
        "BUDOConnection":{
        "@type": "ItemList",
        "itemListElement": [
                       {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "M10"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "SEN.T-B11",
                            "BUDOPositionMedium": "WS.CH.SUP.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"}
                        },
                        
                        {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "M10"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "SEN.T-B01",
                            "BUDOPositionMedium": "WS.H.SUP.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"}
                        },
                        
                        {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "M10"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "SEN.T-B02",
                            "BUDOPositionMedium": "WS.H.RET.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"}
                        },
                        
                        {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "M10"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "HP-K12",
                            "BUDOSubsystem": "SEN.T-B12",
                            "BUDOPositionMedium": "WS.CH.RET.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"}
                        }                  
                        
                      
                           ] },
        "BUDOKey":{
        "@type": "ItemList",
        "itemListElement": [
                       {
        
                        "BUDOBuildingAssignment": "BL-4120",
                        "BUDOSystem": "HP-K12",
                        "BUDOSubsystem": "SEN.VF-85",
                        "BUDOPositionMedium": "WS.H",
                        "BUDOType": "MEA.VF",
                        "BUDOIOFunction": "AI",
                        "itemID": "1757",
                        "multiply": "0.28",
                        "plus":"0"
                        
                                      },
                                
                                      
                      {
                      "BUDOBuildingAssignment": "BL-4120",
                        "BUDOSystem": "HP-K12",
                        "BUDOSubsystem": "SEN.T-B02",
                        "BUDOPositionMedium": "WS.H.RET.PRIM",
                        "BUDOType": "MEA.T",
                        "BUDOIOFunction": "AI",
                        "itemID": "1026",
                        "plus": "273.15",
                        "multiply": "1"
                        
                      
                      },
                      
                      {
                        "BUDOBuildingAssignment": "BL-4120",
                        "BUDOSystem": "HP-K12",
                        "BUDOSubsystem": "SEN.VF-84",
                        "BUDOPositionMedium": "WS.CH",
                        "BUDOType": "MEA.VF",
                        "BUDOIOFunction": "AI",
                        "itemID": "1756",
                        "multiply": "0.28",
                        "plus":"0"
                        
                      
                      },
                      
                      {
                        "BUDOBuildingAssignment": "BL-4120",
                        "BUDOSystem": "HP-K12",
                        "BUDOSubsystem": "SEN.T-B12",
                        "BUDOPositionMedium": "WS.CH.RET.PRIM",
                        "BUDOType": "MEA.T",
                        "BUDOIOFunction": "AI",
                        "itemID": "1036",
                        "plus": "273.15",
                        "multiply":"1"
                       
                      
                      },
                      
                      {
                        "BUDOBuildingAssignment": "BL-4120",
                        "BUDOSystem": "HP-K12C",
                        "BUDOSubsystem": "SEN.POW.H-E100",
                        "BUDOPositionMedium": "WS",
                        "BUDOType": "MEA.POW.H",
                        "BUDOIOFunction": "AI",
                        "itemID": "825",
                        "multiply": "0.01",
                        "plus":"0"
                                              
                      }               
                      
                      ]
                      },
        
        
        "BUDONames":{
        "@type": "ItemList",
        "itemListElement": [
                       {
        
                        "Pump": "PU",
                        "Boiler": "BOI",
                        "Valve": "VAL",
                        "Temperature_Sensor": "MEA.T",
                        "Heat_Pump": "HP",
                        "Combined_Heat_Power": "CHP",
                        "Heat_Exchanger": "HX",
                        "Setpoint": "SEV",
                        "Command":"COM",
                        "Alarm":"AL",
                        "Status":"STAT"
                        
                                      },
                                
                                      
                      {
                              
                      "T_Piece": "TP"                        
                      
                      }
                      
                      
                      ]
                      }
  }
        
        
