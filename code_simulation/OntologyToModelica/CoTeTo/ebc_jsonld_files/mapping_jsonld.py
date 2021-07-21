context_mapping = {
        "schema": "http://www.w3.org/2001/XMLSchema#",
        "brick": "http://brickschema.org/schema/1.0.3/Brick#",
        "brickFrame": "http://brickschema.org/schema/1.0.3/BrickFrame#",
        "BUDO-M": "https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",        
        
        "Equipment": {"@id": "brick: Equipment"},
        "Point": {"@id": "brick: Point"},
        "BUDOSystem": {"@id": "BUDO-M: BUDOSystem"},
        "ModelicaModel": {"@id": "BUDO-M: ModelicaModel"},
        "portHeatflow": {"@id": "BUDO-M: portHeatflow"},
        "EquipmentPointParameter": {"@id": "BUDO-M: EquipmentPointParameter"},
        "EquipmentPointUnits": {"@id": "BUDO-M: EquipmentPointUnits"},
        "EquipmentPointExplanation": {"@id": "BUDO-M: EquipmentPointExplanation"},
        "portParameter": {"@id": "BUDO-M: portParameter"},
        "portUnits": {"@id": "BUDO-M: portUnits"},
        "portExplanation": {"@id": "BUDO-M: portExplanation"},
        "Pump":  {"@id":"brick:Pump"},
        "Boiler":  {"@id":"brick:Boiler"},
        "Valve":  {"@id":"brick:Valve"},
        "Temperature_Sensor":  {"@id":"brick:Temperature_Sensor"},
        "Heat_Pump":  {"@id":"brick:Heat_Pump"},
        "Combined_Heat_Power":  {"@id":"brick:Combined_Heat_Power"},
        "Heat_Exchanger":  {"@id":"brick:Heat_Exchanger"},
        "ItemList": {"@id":"schema:ItemList"},
        "itemListElement": {"@id":"schema:itemListElement"},
        "T_Piece":  {"@id":"BUDO-M:T_Piece"}

           
       
}


doc_mapping_brick={
        "@context": context_mapping,
        
        "@type": "ItemList",
        "itemListElement": [{
            "Pump":{
                        
            "Point":"Hot_Water_Pump/Chilled_Water_Pump", 
            "BUDOSystem":"PU", "ModelicaModel": "1", 
            "portHeatflow": "1", 
            "EquipmentPointParameter":"signalpath.massflow", 
            "EquipmentPointUnits":"kg/s", 
            "EquipmentPointExplanation":"mat file directory for input signal: prescribed mass flow rate for pump", 
            "portParameter":"massFlow.nominal/massFlow.nominal.Pipe.out/pressureDifference.nominal.Pipe.out/medium", 
            "portUnits":"kg/s,kg/s,pa,-", 
            "portExplanation":"-/nominal  mass flow rate in the pipe connected to this port /nominal  pressure drop in the pipe connected to this port /medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity"
            
            } },

        {                
            "Boiler": { 
                    
            "Point":"Boiler", 
            "BUDOSystem":"BOI", 
            "ModelicaModel": "5", 
            "portHeatflow": "1", 
            "EquipmentPointParameter": "signalpath.status/signalpath.mode/signalpath.temperature", 
            "EquipmentPointUnits":"-,-,K", 
            "EquipmentPointExplanation": "mat file directory for input signal: boiler on off status , boolean value required/mat file directory for input signal: boiler switch to night mode, boolean value required/mat file directory for input signal: ambient temperature",
            "portParameter":"massFlow.nominal/massFlow.nominal.Pipe.out/pressureDifference.nominal.Pipe.out/medium", 
            "portUnits":"kg/s,kg/s,pa,-", 
            "portExplanation":"-/nominal  mass flow rate in the pipe connected to this port /nominal  pressure drop in the pipe connected to this port /medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity"
            }
            },
              
            {
            "Valve": { 
                    
            "Point":"Heating_Valve", 
            "BUDOSystem":"VAL", 
            "ModelicaModel": "1", 
            "portHeatflow": "2", 
            "EquipmentPointParameter":"signalpath.position", 
            "EquipmentPointUnits":"-", 
            "EquipmentPointExplanation":"mat file directory for input signal: actuator position,  value in range [0,1] required  (0: closed, 1: open)", 
            "portParameter":"massFlow.nominal/pressureDifference.nominal/massFlow.nominal.Pipe.out/pressureDifference.nominal.Pipe.out/medium",
            "portUnits":"kg/s,pa,kg/s,pa,-",
            "portExplanation":"-/-/nominal  mass flow rate in the pipe connected to this port /nominal  pressure drop in the pipe connected to this port /medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity"
            }
            },
               
            {
            "Temperature_Sensor": { 
            
            "Point":"Hot_Water_Supply_Temperature_Sensor/Hot_Water_Return_Temperature_Sensor/Chilled_Water_Supply_Temperature_Sensor/Chilled_Water_Return_Temperature_Sensor", 
            "BUDOSystem":"MEA.T", 
            "ModelicaModel": "0", 
            "portHeatflow": "0", 
            "EquipmentPointParameter": "massFlow.nominal/medium", 
            "EquipmentPointUnits": "kg/s,-", 
            "EquipmentPointExplanation":"- /medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity", 
            "portParameter":"",
            "portUnits":"",
            "portExplanation":""
            }
            },
                    
            {        
            "Heat_Pump": { 
                    
            "Point":"Heat_Pump", 
            "BUDOSystem":"HP", 
            "ModelicaModel": "1", 
            "portHeatflow": "2", 
            "EquipmentPointParameter":"CoefficientOfPerformance/compressorPower.nominal/signalpath.loadratio", 
            "EquipmentPointUnits":"-,W,-", 
            "EquipmentPointExplanation":"-/-/mat file directory for input signal: part load ratio of compressor in heat pump, value in range [0,1] required", 
            "portParameter":"massFlow.nominal/pressureDifference.nominal/massFlow.nominal.Pipe.out/pressureDifference.nominal.Pipe.out/temperatureDifference.nominal/temperature.average.nominal/medium", 
            "portUnits":"kg/s,pa,kg/s,pa,K,K,-", 
            "portExplanation":"-/-/nominal  mass flow rate in the pipe connected to this port /nominal  pressure drop in the pipe connected to this port /temperature difference  outlet-inlet in condenser for portHeatflow.prim, in evaporator for portHeatflow .sec/nominal average temperature  in condenser for portHeatflow.prim, in evaporator for portHeatflow .sec/medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity"
            }
            
            },
                    
            {        
            "Combined_Heat_Power": { 
                    
            "Point":"Combined_Heat_Power", 
            "BUDOSystem":"CHP", 
            "ModelicaModel": "3", 
            "portHeatflow":"1", 
            "EquipmentPointParameter":"signalpath.status/signalpath.temperature", 
            "EquipmentPointUnits":"-,K", 
            "EquipmentPointExplanation":"mat file directory for input signal: CHP on off status, boolean value required/mat file directory for input signal: CHP temperature setpoint, boolean value required", 
            "portParameter":"massFlow.nominal/medium", 
            "portUnits":"kg/s,-", 
            "portExplanation":"-/medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity"
            }
            },
                    
            {        
            "Heat_Exchanger": { 
                    
            "Point":"Heat_Exchanger", 
            "BUDOSystem":"HX", 
            "ModelicaModel":"0", 
            "portHeatflow":"2", 
            "EquipmentPointParameter":"",
            "EquipmentPointUnits":"",
            "EquipmentPointExplanation":"", 
            "portParameter":"massFlow.nominal/pressureDifference.nominal/massFlow.nominal.Pipe.out/pressureDifference.nominal.Pipe.out/medium", 
            "portUnits":"kg/s,pa,kg/s,pa,K,K,-", 
            "portExplanation":"-/-/nominal  mass flow rate in the pipe connected to this port /nominal  pressure drop in the pipe connected to this port /-/-/medium flowing in this component, example: AixLib.Media.Specialized.Water.TemperatureDependentDensity "
            }
            



                            }]

                                        }


doc_mapping_BUDO={
        
        "@context": context_mapping,
        
        "@type": "ItemList",
        "itemListElement": [
            
                
            {
            
        
            "T_Piece": { 
                
            "Point":"T_Piece", 
            "BUDOSystem":"TP", 
            "ModelicaModel": "0", 
            "portHeatflow": "2", 
            "EquipmentPointParameter": "0", 
            "EquipmentPointUnits": "0", 
            "EquipmentPointExplanation": "0", 
            "portParameter": "medium", 
            "portUnits":"-", 
            "portExplanation":"medium in modelica model"
            
            }
                 }
                   
         
          
            ]


                                }


        
        