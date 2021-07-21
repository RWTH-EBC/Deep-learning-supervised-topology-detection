<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject1=instance+"_PH.PRIM"
subject2=instance+"_PH.SEC"
m1_flow_nominal=func.get_data_property(subject1,"massFlow.nominal",g,3)
m2_flow_nominal=func.get_data_property(subject2,"massFlow.nominal",g,3)
medium1=func.get_data_property(subject1,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
medium2=func.get_data_property(subject2,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
dp1_nominal=func.get_data_property(subject1,"pressureDifference.nominal",g,10000)
dp2_nominal=func.get_data_property(subject2,"pressureDifference.nominal",g,10000)
dTCon_nominal=func.get_data_property(subject1,"temperatureDifference.nominal",g,10)
dTEva_nominal=func.get_data_property(subject2,"temperatureDifference.nominal",g,-5)
TCon_nominal=func.get_data_property(subject1,"temperature.average.nominal",g,303.15)
TEva_nominal=func.get_data_property(subject2,"temperature.average.nominal",g,278.15)
P_nominal=func.get_data_property(instance,"compressorPower.nominal",g,30000)
COP_nominal=func.get_data_property(instance,"CoefficientOfPerformance",g,3.15)
signalpath.loadratio=func.get_data_property(instance,"signalpath.loadratio",g,None)
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
%>
AixLib.Fluid.HeatPumps.Carnot_y Heat_Pump${number}(
    redeclare package Medium1 = ${medium1},
    redeclare package Medium2 = ${medium2},
    dp1_nominal=${dp1_nominal},
    dp2_nominal=${dp2_nominal},
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    show_T=true,
    dTEva_nominal=${dTEva_nominal},
    dTCon_nominal=${dTCon_nominal},
    P_nominal=${P_nominal},
    m1_flow_small=${m1_flow_nominal},
    m2_flow_small=${m2_flow_nominal},
    use_eta_Carnot_nominal=false,
    COP_nominal=${COP_nominal},
    TCon_nominal=${TCon_nominal},
    TEva_nominal=${TEva_nominal},
    homotopyInitialization=true)
    "${instance}"
    annotation (Placement(transformation(extent={${lu},${ro}})));
	
	
% if signalpath.loadratio==None:	
Modelica.Blocks.Sources.Ramp uCom${number}(
    height=0.8,
    duration=60,
    offset=0,
    startTime=1800) "Compressor control signal"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));
% else:
<%func.add_combitimetable(instance,instancedic,number,'uCom',signalpath.loadratio,1)%>
% endif

