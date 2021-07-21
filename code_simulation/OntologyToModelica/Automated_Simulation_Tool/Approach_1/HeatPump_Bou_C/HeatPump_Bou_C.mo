within ;
model HeatPump_Bou_C






































































































inner Modelica.Fluid.System system
 annotation (Placement(transformation(extent={{-98,60},{-78,80}})));































Modelica.Fluid.Sources.MassFlowSource_T source1(
    nPorts=1,
    use_m_flow_in=true,
    use_T_in=true,
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity)
 "source feed BL-4120_._HP-K12_-M10_PH.PRIM"
 annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=180,
        origin={60,-38})));

Modelica.Blocks.Sources.CombiTimeTable boundarytemperature1(
 smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
 extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
 tableOnFile=true,
 verboseRead=false,
 tableName="data",
 columns=1:1,
 offset={0,0},
    fileName=
        "C:/Users/fst-bll.EONERC/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/HeatPump_Bou_C/1026.mat")
     annotation (Placement(transformation(extent={{70,52},{90,72}})));
Modelica.Blocks.Sources.CombiTimeTable boundarymassflow1(
 smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
 extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
 tableOnFile=true,
 verboseRead=false,
 tableName="data",
 columns=1:2,
 offset={0,0},
    fileName=
        "C:/Users/fst-bll.EONERC/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/HeatPump_Bou_C/1757.mat")
     annotation (Placement(transformation(extent={{30,70},{50,90}})));





























Modelica.Fluid.Sources.MassFlowSource_T source2(
    nPorts=1,
    use_m_flow_in=true,
    use_T_in=true,
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity)
 "source feed BL-4120_._HP-K12_-M10_PH.SEC"
 annotation (Placement(transformation(extent={{-86,-62},{-66,-42}})));

Modelica.Blocks.Sources.CombiTimeTable boundarytemperature2(
 smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
 extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
 tableOnFile=true,
 verboseRead=false,
 tableName="data",
 columns=1:1,
 offset={0,0},
    fileName=
        "C:/Users/fst-bll.EONERC/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/HeatPump_Bou_C/1036.mat")
     annotation (Placement(transformation(extent={{-72,28},{-92,48}})));
Modelica.Blocks.Sources.CombiTimeTable boundarymassflow2(
 smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
 extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
 tableOnFile=true,
 verboseRead=false,
 tableName="data",
 columns=1:2,
 offset={0,0},
    fileName=
        "C:/Users/fst-bll.EONERC/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/HeatPump_Bou_C/1756.mat")
     annotation (Placement(transformation(extent={{-10,10},{10,-10}},
        rotation=180,
        origin={-50,72})));





















AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor1(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=8.81,tau=0)
 "BL-4120_._HP-K12_SEN.T-B02_WS.H.RET.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{28,-18},{48,2}})));















AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor2(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=6.17,tau=0)
 "BL-4120_._HP-K12_SEN.T-B12_WS.CH.RET.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{-30,-62},{-10,-42}})));















AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor3(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=8.81,tau=0)
 "BL-4120_._HP-K12_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{-32,12},{-12,32}})));















AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor4(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=6.17,tau=0)
 "BL-4120_._HP-K12_SEN.T-B11_WS.CH.SUP.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{58,26},{78,46}})));









































































AixLib.Fluid.HeatPumps.Carnot_y Heat_Pump1(
    redeclare package Medium1 =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    redeclare package Medium2 =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    COP_nominal=6.4,
    P_nominal=29000,
    dTCon_nominal=5,
    dTEva_nominal=-6,
    dp1_nominal=2700,
    dp2_nominal=3900,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    homotopyInitialization=true,
    m1_flow_small=7.63,
    m2_flow_small=9.05,
    show_T=true,
    use_eta_Carnot_nominal= true,
    TCon_nominal=305.65,
    TEva_nominal=281.65)
    "BL-4120_._HP-K12_-M10"
    annotation (Placement(transformation(extent={{22,38},{2,58}})));



Modelica.Blocks.Sources.CombiTimeTable uCom1(
 smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
 extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
 tableOnFile=true,
 verboseRead=false,
 tableName="data",
 columns=1:1,
 offset={0,0},
    fileName=
        "C:/Users/fst-bll.EONERC/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/HeatPump_Bou_C/825.mat")
 annotation (Placement(transformation(extent={{-24,74},{-4,94}})));



















































Modelica.Fluid.Sources.Boundary_pT sink1(
  nPorts=1, redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity)
 "sink isFedby BL-4120_._HP-K12_-M10_PH.PRIM"
 annotation (Placement(transformation(extent={{-58,-22},{-38,-2}})));









Modelica.Fluid.Sources.Boundary_pT sink2(
  nPorts=1, redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity)
 "sink isFedby BL-4120_._HP-K12_-M10_PH.SEC"
 annotation (Placement(transformation(extent={{58,-8},{78,12}})));


equation










connect(uCom1.y[2],Heat_Pump1. y)
  annotation (Line(points={{-3,84},{24,84},{24,57}},
                                              color={0,0,127}));















connect(Heat_Pump1.port_a1, Temperature_Sensor1.port_b)
 annotation (Line(points={{22,54},{22,54},{22,-8},{48,-8}},
                                             color={0,127,255}));








connect(Heat_Pump1.port_b1, Temperature_Sensor3.port_a)
 annotation (Line(points={{2,54},{-32,54},{-32,22}},
                                            color={0,127,255}));








connect(Heat_Pump1.port_b2, Temperature_Sensor4.port_a)
 annotation (Line(points={{22,42},{32,42},{32,36},{58,36}},
                                             color={0,127,255}));








connect(Heat_Pump1.port_a2, Temperature_Sensor2.port_b)
 annotation (Line(points={{2,42},{2,-52},{-10,-52}},
                                             color={0,127,255}));










connect(source1.ports[1],Temperature_Sensor1.port_a)
 annotation (Line(points={{50,-38},{22,-38},{22,-8},{28,-8}},
                                            color={0,127,255}));
connect(boundarytemperature1.y[2], source1.T_in)
 annotation (Line(points={{91,62},{92,62},{92,-42},{72,-42}},
                                              color={0,0,127}));
connect(boundarymassflow1.y[2], source1.m_flow_in)
 annotation (Line(points={{51,80},{98,80},{98,-46},{70,-46}},
                                             color={0,0,127}));


connect(source2.ports[1],Temperature_Sensor2.port_a)
 annotation (Line(points={{-66,-52},{-30,-52}},
                                             color={0,127,255}));
connect(boundarytemperature2.y[2], source2.T_in)
 annotation (Line(points={{-93,38},{-96,38},{-96,-48},{-88,-48}},
                                             color={0,0,127}));
connect(boundarymassflow2.y[2], source2.m_flow_in)
 annotation (Line(points={{-61,72},{-64,72},{-64,-44},{-86,-44}},
                                             color={0,0,127}));


connect(Temperature_Sensor3.port_b,sink1.ports[1])
 annotation (Line(points={{-12,22},{-32,22},{-32,-12},{-38,-12}},
                                            color={0,127,255}));


connect(Temperature_Sensor4.port_b,sink2.ports[1])
 annotation (Line(points={{78,36},{78,18},{84,18},{84,2},{78,2}},
                                            color={0,127,255}));

 annotation (uses(                         Modelica(version="3.2.2"), AixLib(
          version="0.7.3")),
    version="1",
    conversion(noneFromVersion=""));
end HeatPump_Bou_C;
