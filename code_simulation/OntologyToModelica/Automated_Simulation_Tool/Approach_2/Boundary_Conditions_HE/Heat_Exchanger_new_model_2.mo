within ;
model Heat_Exchanger_new_model_2

inner Modelica.Fluid.System system
 annotation (Placement(transformation(extent={{-180,80},{-160,100}})));

AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor3(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=14.08,tau=0)
 "BL-4120_._HX-H03_SEN.T-B03_WS.H.SUP.SEC_MEA.T_AI"
 annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=0,
        origin={44,-4})));

AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor4(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=6.13,tau=0)
 "BL-4120_._HX-H03_SEN.T-B02_WS.H.RET.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{30,46},{50,66}})));

AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor2(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=14.08,tau=0)
 "BL-4120_._HX-H03_SEN.T-B04_WS.H.RET.SEC_MEA.T_AI"
 annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=0,
        origin={-60,-4})));

AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor1(
 redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
 m_flow_nominal=6.13,tau=0)
 "BL-4120_._HX-H03_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI"
 annotation (Placement(transformation(extent={{-70,42},{-50,62}})));

AixLib.Fluid.HeatExchangers.ConstantEffectiveness Heat_Exchanger1(
    redeclare package Medium1 =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    redeclare package Medium2 =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    show_T=true,
    m1_flow_nominal=6.13,
    m2_flow_nominal=14.08,
    dp1_nominal(displayUnit="Pa") = 14000,
    dp2_nominal(displayUnit="Pa") = 48000,
    eps=0.7)
 "BL-4120_._HX-H03_-WT03"
    annotation (Placement(transformation(extent={{-22,18},{-2,38}})));

Modelica.Fluid.Sources.Boundary_pT sink1(
            redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity, nPorts=1)
 "sink isFedby BL-4120_._HX-H03_VAL.CTRL-Y01_WS.H.RET.PRIM_PH"
 annotation (Placement(transformation(extent={{88,62},{68,82}})));

Modelica.Fluid.Sources.Boundary_pT sink2(
            redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity, nPorts=1)
 "sink isFedby BL-4120_._HX-H03_TP.MX-T01_WS.H.RET.SEC_PH.PRIM"
 annotation (Placement(transformation(extent={{10,-10},{-10,10}},
        rotation=180,
        origin={-126,-4})));

Modelica.Blocks.Sources.CombiTimeTable massflow1(
    smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
    extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
    tableOnFile=true,
    verboseRead=false,
    tableName="data",
    columns=1:1,
    offset={0,0},
    fileName=
        "N:/Forschung/EBC0400_BMWI_OOM4ABDO_UES_GA/Students/fst-bll/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/After_Bergfest/Boundary_Conditios_HE/1755_week_test.mat")
 annotation (Placement(transformation(extent={{10,10},{-10,-10}},
        rotation=180,
        origin={-140,88})));
Modelica.Blocks.Sources.CombiTimeTable boundarytemperature1(
    smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
    extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
    tableOnFile=true,
    verboseRead=false,
    tableName="data",
    columns=1:1,
    offset={0,0},
    fileName=
        "N:/Forschung/EBC0400_BMWI_OOM4ABDO_UES_GA/Students/fst-bll/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/After_Bergfest/Boundary_Conditios_HE/260_week_test.mat")
     annotation (Placement(transformation(extent={{-152,22},{-132,42}})));
Modelica.Blocks.Sources.CombiTimeTable massflow3(
    smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
    extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
    tableOnFile=true,
    verboseRead=false,
    tableName="data",
    columns=1:1,
    offset={0,0},
    fileName=
        "N:/Forschung/EBC0400_BMWI_OOM4ABDO_UES_GA/Students/fst-bll/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/After_Bergfest/Boundary_Conditios_HE/1754_week_test.mat")
 annotation (Placement(transformation(extent={{100,-56},{120,-36}})));
Modelica.Blocks.Sources.CombiTimeTable boundarytemperature3(
    smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
    extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
    tableOnFile=true,
    verboseRead=false,
    tableName="data",
    columns=1:1,
    offset={0,0},
    fileName=
        "N:/Forschung/EBC0400_BMWI_OOM4ABDO_UES_GA/Students/fst-bll/sciebo3/MT/Machine-Learning/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/Simulations/After_Bergfest/Boundary_Conditios_HE/264_week_test.mat")
     annotation (Placement(transformation(extent={{98,28},{118,48}})));
  Modelica.Fluid.Sources.MassFlowSource_T source1(
    redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    use_m_flow_in=true,
    use_T_in=true,
    nPorts=1)
    annotation (Placement(transformation(extent={{-104,42},{-84,62}})));
  Modelica.Fluid.Sources.MassFlowSource_T source2(
    redeclare package Medium =
        AixLib.Media.Specialized.Water.TemperatureDependentDensity,
    use_m_flow_in=true,
    use_T_in=true,
    nPorts=1) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={96,-4})));
equation

connect(Heat_Exchanger1.port_a1,Temperature_Sensor1. port_b)
 annotation (Line(points={{-22,34},{-36,34},{-36,52},{-50,52}},
                                                color={0,127,255}));

connect(Heat_Exchanger1.port_b1,Temperature_Sensor4. port_a)
 annotation (Line(points={{-2,34},{8,34},{8,56},{30,56}},
                                            color={0,127,255}));

connect(Heat_Exchanger1.port_a2,Temperature_Sensor3. port_b)
 annotation (Line(points={{-2,22},{14,22},{14,-4},{54,-4}},
                                              color={0,127,255}));

connect(Heat_Exchanger1.port_b2,Temperature_Sensor2. port_a)
 annotation (Line(points={{-22,22},{-30,22},{-30,-4},{-70,-4}},
                                             color={0,127,255}));

  connect(Temperature_Sensor2.port_b, sink2.ports[1]) annotation (Line(points={
          {-50,-4},{-88,-4},{-88,-4},{-116,-4}}, color={0,127,255}));
  connect(Temperature_Sensor4.port_b, sink1.ports[1]) annotation (Line(points={
          {50,56},{58,56},{58,72},{68,72}}, color={0,127,255}));
  connect(source1.ports[1], Temperature_Sensor1.port_a)
    annotation (Line(points={{-84,52},{-70,52}}, color={0,127,255}));
  connect(massflow1.y[2], source1.m_flow_in) annotation (Line(points={{-129,88},
          {-120,88},{-120,60},{-104,60}}, color={0,0,127}));
  connect(boundarytemperature1.y[2], source1.T_in) annotation (Line(points={{
          -131,32},{-124,32},{-124,56},{-106,56}}, color={0,0,127}));
  connect(source2.ports[1], Temperature_Sensor3.port_b)
    annotation (Line(points={{86,-4},{54,-4}}, color={0,127,255}));
  connect(boundarytemperature3.y[2], source2.T_in) annotation (Line(points={{
          119,38},{126,38},{126,-8},{108,-8}}, color={0,0,127}));
  connect(massflow3.y[2], source2.m_flow_in) annotation (Line(points={{121,-46},
          {126,-46},{126,-12},{106,-12}}, color={0,0,127}));
 annotation (uses(AixLib(version="0.5.2"), Modelica(version="3.2.2")),
    Diagram(coordinateSystem(extent={{-180,-120},{180,120}})),
    Icon(coordinateSystem(extent={{-180,-120},{180,120}})),
    experiment(
      StopTime=604800,
      __Dymola_NumberOfIntervals=300,
      Tolerance=1e-06));
end Heat_Exchanger_new_model_2;
