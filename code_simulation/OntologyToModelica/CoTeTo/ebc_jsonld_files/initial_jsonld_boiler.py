####           BOILER        #####

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
        "BUDONames":  {"@id":"BUDO-M:BUDONames"},
        "feeds": {"@id":"brick:feeds"},
        "portHeatflow.prim_1": {"@id":"BUDO-M:portHeatflow.prim_1"},
        "portHeatflow.prim_2": {"@id":"BUDO-M:portHeatflow.prim_2"},
        "portHeatflow.sec_1": {"@id":"BUDO-M:portHeatflow.sec_1"},
        "portHeatflow.sec_2": {"@id":"BUDO-M:portHeatflow.sec_2"}
                    
}


doc = {
    
        "@context": context,
        "Zone":"H02.1",
        
        "BUDOConnection":{
        "@type": "ItemList",
        "itemListElement": [
                       {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "M01"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "SEN.T-B06",
                            "BUDOPositionMedium": "WS.H.RET.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"}
                        },
                        
                        {
            
                        "Equipment": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "TP.DIV-T01"},
                        
                        "ConnectionType": {"@type": "hasPoint"},
                            
                        "Point": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "SEN.T-B01",
                            "BUDOPositionMedium": "WS.H.SUP.PRIM",
                            "BUDOType": "MEA.T",
                            "BUDOIOFunction": "AI"} 
                        },
                        
                        {
            
                        "portHeatflow.prim_1": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "CTRL-A01"},
                        
                        "ConnectionType": {"@type": "feeds"},
                            
                        "portHeatflow.prim_2": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "TP.DIV-T01",
                            "BUDOPositionMedium": "WS.H.RET.PRIM"
                            }
                        },
                        
                        {
            
                        "portHeatflow.prim_1": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "VAL.MX-Y01"},
                        
                        "ConnectionType": {"@type": "feeds"},
                            
                        "portHeatflow.prim_2": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "PU-M01"
                            }
                        } ,
                        
                        {
            
                        "portHeatflow.prim_1": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "PU-M01"},
                        
                        "ConnectionType": {"@type": "feeds"},
                            
                        "portHeatflow.prim_2": {
                             "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "CTRL-A01"}
                            
                        },
                        
                        {
            
                        "portHeatflow.sec_1": {                            
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "TP.DIV-T01"},
                        
                        "ConnectionType": {"@type": "feeds"},
                            
                        "portHeatflow.sec_2": {
                            "BUDOBuildingAssignment": "BL-4120",
                            "BUDOSystem": "BOI.COND-H02.1",
                            "BUDOSubsystem": "VAL.MX-Y01"}
                            }
                                   
                        
                      
                           ] },
        
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
        
        
