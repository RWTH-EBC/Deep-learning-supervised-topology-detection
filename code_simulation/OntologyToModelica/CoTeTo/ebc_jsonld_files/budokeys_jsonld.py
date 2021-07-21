context_keys = {
        "schema": "http://www.w3.org/2001/XMLSchema#",
        "brick": "http://brickschema.org/schema/1.0.3/Brick#",
        "brickFrame": "http://brickschema.org/schema/1.0.3/BrickFrame#",
        "BUDO-M": "https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        
        
        "BUDOKey": {"@id": "BUDO-M: BUDOKey"},
        "BUDOBuildingAssignment": {"@id": "BUDO-M: BUDOBuildingAssignment"},
        "BUDOSystem": {"@id": "BUDO-M: BUDOSystem"},
        "BUDOSubsystem": {"@id": "BUDO-M: BUDOSubsystem"},
        "BUDOPositionMedium": {"@id": "BUDO-M: BUDOPositionMedium"},
        "BUDOType": {"@id": "BUDO-M: BUDOType"},
        "BUDOIOFunction": {"@id": "BUDO-M: BUDOIOFunction"},
        "itemID": {"@id": "BUDO-M: ItemID"},
        "ItemList": {"@id":"schema:ItemList"},
        "itemListElement": {"@id":"schema:itemListElement"},
        "Pump":  {"@id":"brick:Pump"},
        "Boiler":  {"@id":"brick:Boiler"},
        "Valve":  {"@id":"brick:Valve"},
        "Temperature_Sensor":  {"@id":"brick:Temperature_Sensor"},
        "Heat_Pump":  {"@id":"brick:Heat_Pump"},
        "Combined_Heat_Power":  {"@id":"brick:Combined_Heat_Power"},
        "Heat_Exchanger":  {"@id":"brick:Heat_Exchanger"}   
        
       
}


doc_keys = {
    
        "@context": context_keys,
        
        "@type": "ItemList",
        "itemListElement": [{
                "Boiler":{
                "@type": "ItemList",
                "itemListElement": [               
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_VAL.MX-Y01_WS.H.RET.PRIM_SEV.POS_AO",
                            "itemID": "232"},                        
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_VAL.MX-Y02_WS.H.SUP.PRIM_SEV.POS_AO",
                            "itemID": "233"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI",
                             "itemID":"234"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_SEN.T-B02_WS.H.SUP.PRIM_MEA.T_AI",
                             "itemID":"235"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_SEN.T-B03_HYDS_MEA.T_AI",
                             "itemID":"236"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI",
                             "itemID":"237"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_SEN.T-B07_WS.H.RET.PRIM_MEA.T_AI",
                             "itemID":"238"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_CTRL-A01_COM.CLEA_BO",
                             "itemID":"239"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_PU-M01_WS.H.RET.PRIM_COM_BO",
                             "itemID":"240"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_PU-M02_WS.H.RET.PRIM_COM_BO",
                             "itemID":"241"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_SW.EMR_AL.EMR_BI",
                             "itemID":"242"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_CTRL-A01_STAT_BI",
                             "itemID":"243"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_CTRL-A01_STAT_BI",
                             "itemID":"244"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_CTRL-A02_STAT_BI",
                             "itemID":"245"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_PU-M01_WS.H.RET.PRIM_STAT_BI",
                             "itemID":"246"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_PU-M02_WS.H.RET.PRIM_STAT_BI",
                             "itemID":"248"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_CTRL-A01_AL_BI",
                             "itemID":"250"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_PU-M01_WS.H.RET.PRIM_AL_BI",
                             "itemID":"251"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.2_PU-M02_WS.H.SUP_AL_BI",
                             "itemID":"252"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_CTRL_COM.CLEA_",
                             "itemID":"253"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02_SEN.VF-77_WS.H_MEA.VF_AI",
                             "itemID":"1749"},
                            {"BUDOKey":"BL-4120_._BOI.COND-H02.1_TP.DIV-T01_WS.H.RET.PRIM",
                             "itemID":"0"}
                                                    
                                                                ]},
                "Heat_Pump": {
                "@type": "ItemList",
                "itemListElement": [               
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M01_WS.H.RET.PRIM_SEV_AO",
                            "itemID":"1017"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M02_WS.CH.RET.PRIM_SEV_AO",
                            "itemID":"1018"},
                           {"BUDOKey":"BL-4120_._HP-K12_VAL.CTRL-Y01_WS.H.SUP.PRIM_SEV_AO",
                            "itemID":"1021"},
                           {"BUDOKey":"BL-4120_._HP-K12_VAL.CTRL-Y02_WS.CH.SUP.SEC_SEV_AO",
                            "itemID":"1023"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI",
                            "itemID":"1025"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B02_WS.H.RET.PRIM_MEA.T_AI",
                            "itemID":"1026"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B03_WS.H.SUP.SEC_MEA.T_AI",
                            "itemID":"1027"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B06_STO.H.BOT_MEA.T_AI",
                            "itemID":"1028"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B07_STO.H.MID_MEA.T_AI",
                            "itemID":"1030"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B08_STO.H.MID_MEA.T_AI",
                            "itemID":"1031"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B09_STO.H.TOP_MEA.T_AI",
                            "itemID":"1032"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B11_WS.CH.SUP.PRIM_MEA.T_AI",
                            "itemID":"1034"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B12_WS.CH.RET.PRIM_MEA.T_AI",
                            "itemID":"1036"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B13_WS_MEA.T_AI",
                            "itemID":"1038"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B16_STO.C.BOT_MEA.T_AI",
                            "itemID":"1039"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B17_STO.C.MID_MEA.T_AI",
                            "itemID":"1041"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B18_STO.C.MID_MEA.T_AI",
                            "itemID":"1042"},
                           {"BUDOKey":"BL-4120_._HP-K12_SEN.T-B19_STO.C.TOP_MEA.T_AI",
                            "itemID":"1043"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL01_WS.H.RET.PRIM_COM_BO",
                            "itemID":"1045"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL02_WS.C.RET.SEC_COM_BO",
                            "itemID":"1046"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M01_WS.H.RET.PRIM_COM_BO",
                            "itemID":"1047"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M02_WS.CH.RET.PRIM_COM_BO",
                            "itemID":"1048"},
                           {"BUDOKey":"BL-4120_._HP-K12_-M10_COM.CLEA_BO",
                            "itemID":"1049"},
                           {"BUDOKey":"BL-4120_._HP-K12_-M10_COM.MOD_BO",
                            "itemID":"1050"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL01_WS.H.RET.PRIM_STAT.OP_BI",
                            "itemID":"1051"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL01_WS.H.RET.PRIM_STAT.CL_BI",
                            "itemID":"1052"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL02_WS.CH.RET.SEC_STAT.OP_BI",
                            "itemID":"1053"},
                           {"BUDOKey":"BL-4120_._HP-K12_DAMP.SHOFF-KL02_WS.CH.RET.SEC_STAT.CL_BI",
                            "itemID":"1054"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M01_WS.H.RET.PRIM_STAT_BI",
                            "itemID":"1055"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M02_WS.CH.RET.PRIM_STAT_BI",
                            "itemID":"1056"},
                           {"BUDOKey":"BL-4120_._HP-K12_M10_STAT_BI",
                            "itemID":"1057"},
                           {"BUDOKey":"BL-4120_._HP-K12_-M10_SEV.MOD.SU_BI",
                            "itemID":"1058"},
                           {"BUDOKey":"BL-4120_._HP-K12_-M10_SEV.MOD.WI_BI",
                            "itemID":"1059"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M01_WS.H.RET.PRIM_AL_BI",
                            "itemID":"1060"},
                           {"BUDOKey":"BL-4120_._HP-K12_PU-M02_WS.CH.RET.PRIM_AL_BI",
                            "itemID":"1061"},
                           {"BUDOKey":"BL-4120_._HP-K12_-M10_AL_BI",
                            "itemID":"1062"}
                                                    
                                                                ]},
                
                "Combined_Heat_Power": {
                "@type": "ItemList",
                "itemListElement": [               
                            
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_SEV.T_AO",
                         "itemID":"212"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI",
                         "itemID":"213"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T-B02_WS.H.RET.PRIM_MEA.T_AI",
                         "itemID":"214"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T-B04_STO..RET.PRIM_MEA.T_AI",
                         "itemID":"215"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T-B05_WS.H.SUP.SEC_MEA.T_AI",
                         "itemID":"216"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T-B06_WS.H.RET.SEC_MEA.T_AI",
                         "itemID":"217"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_COM_BO",
                         "itemID":"218"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_COM.OPR.SUBS_BO",
                         "itemID":"220"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_COM.OPR.MAIN_BO",
                         "itemID":"221"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_AL_BI",
                         "itemID":"222"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL-A01_STAT_BI",
                         "itemID":"223"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.T_AIR_MEA.T_AI",
                         "itemID":"225"},
                        {"BUDOKey":"BL-4120_._CHP-H01-Stufe1_COM_",
                         "itemID":"226"},
                        {"BUDOKey":"BL-4120_._CHP-H01-Stufe2_COM_",
                         "itemID":"227"},
                        {"BUDOKey":"BL-4120_._CHP-H01_CTRL_COM.CLEA_",
                         "itemID":"228"},
                        {"BUDOKey":"BL-4120_._CHP-H01_AL.GAS_",
                         "itemID":"229"},
                        {"BUDOKey":"BL-4120_._CHP-H01_COM.CLEA_SAI",
                         "itemID":"230"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.VF-79_WS.H_MEA.VF_AI",
                         "itemID":"1751"},
                        {"BUDOKey":"BL-4120_._CHP-H01_SEN.VF-78_WS.H_MEA.VF_AI",
                         "itemID":"1750"}
                        

                                                    
                                                                ]},
                "Heat_Exchanger": {
                "@type": "ItemList",
                "itemListElement": [               
                            {"BUDOKey":"BL-4120_._HX-H03_VAL.CTRL-Y01_WS.H.RET.PRIM_SEV.POS_AO",
                             "itemID":"256"},
                            {"BUDOKey":"BL-4120_._HX-H03_VAL.DIV-Y02_WS.H.SUP.SEC_SEV.POS_AO",
                             "itemID":"258"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI",
                             "itemID":"260"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B02_WS.H.RET.PRIM_MEA.T_AI",
                             "itemID":"262"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B03_WS.H.SUP.SEC_MEA.T_AI",
                             "itemID":"264"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B04_WS.H.RET.SEC_MEA.T_AI",
                             "itemID":"266"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B05_WS.H.SUP.SEC_MEA.T_AI",
                             "itemID":"267"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.T-B06_WS.H.SUP.PRIM_MEA.T_AI",
                             "itemID":"269"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M01_WS.H.SUP.PRIM_COM.CLEA_BO",
                             "itemID":"270"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M02_WS.H.SEC_COM.CLEA_BO",
                             "itemID":"271"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.P.DIF-W01_WS.H.PRIM_AL.P.MIN_BI",
                             "itemID":"273"},
                            {"BUDOKey":"BL-4120_._HX-H03_SEN.P.DIF-W02_WS.H.SEC_AL.P.MIN_BI",
                             "itemID":"274"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M01_WS.H.SUP.PRIM_STAT_BI",
                             "itemID":"275"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M02_WS.H.SEC_STAT_BI",
                             "itemID":"276"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M01_WS.H.SUP.PRIM_AL_BI",
                             "itemID":"277"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M02_WS.H.SEC_AL_BI",
                             "itemID":"278"},
                            {"BUDOKey":"BL-4120_._HX-H03_PU-M02_WS.H.SEC_COM_BO",
                             "itemID":"279"},
                            {"BUDOKey":"BL-4120_._HX-H03_TP.MX-T01_WS.H.RET.SEC",
                             "itemID":"0"},
                            {"BUDOKey":"BL-4120_._HX-H03_-WT03",
                             "itemID":"0"}
                                                    
                                                                ]}
                
                   
                
                
                } ]
                              
   }
                
                
                
                



















   

