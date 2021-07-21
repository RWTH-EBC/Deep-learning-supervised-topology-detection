<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject=instance+"_PH"
m_flow_nominal=func.get_data_property(subject,"massFlow.nominal",g,3)
medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.status=func.get_data_property(instance,"signalpath.status",g,None)
signalpath.temperature=func.get_data_property(instance,"signalpath.temperature",g,None)
signalpath.mode=func.get_data_property(instance,"signalpath.mode",g,None)
%>

AixLib.Fluid.BoilerCHP.Boiler Boiler${number}(
	redeclare package Medium =${medium}, paramBoiler=
    AixLib.DataBase.Boiler.General.Boiler_Vitocrossal200_311kW(),
    paramHC=AixLib.DataBase.Boiler.DayNightMode.HeatingCurves_Vitotronic_Day23_Night10(),
    m_flow_nominal=${m_flow_nominal})
	"${instance}"
    annotation (Placement(transformation(extent={${lu},${ro}})));
	
% if signalpath.status==None:	
Modelica.Blocks.Sources.BooleanConstant isOn${number}
    "Boiler is always on"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));
% else:
<%func.add_combitimetable(instance,instancedic,number,'isOn',signalpath.status,1)%>
<%func.real_to_boolean(instance,instancedic,'isOnBoolean',number,2)%>
% endif	
	
	
% if signalpath.temperature==None:
Modelica.Blocks.Sources.Sine TAmbient${number}(
    amplitude=5,
    freqHz=1/86400,
    phase=4.7123889803847,
    offset=273.15)
    "Ambient air temperature"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][3]['position'][0]},${instancedic[instance]['add'][3]['position'][1]}})));
% else:
<%func.add_combitimetable(instance,instancedic,number,'TAmbient',signalpath.temperature,3)%>
% endif

% if signalpath.mode==None:		
Modelica.Blocks.Sources.BooleanConstant switchToNightMode${number}(k=false)
    "No night-setback"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][4]['position'][0]},${instancedic[instance]['add'][4]['position'][1]}})));	
% else:
<%func.add_combitimetable(instance,instancedic,number,'switchToNightMode',signalpath.mode,4)%>
<%func.real_to_boolean(instance,instancedic,'switchToNightModeBoolean',number,5)%>
% endif

