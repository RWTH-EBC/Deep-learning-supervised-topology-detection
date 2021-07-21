<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject=instance+"_PH"
m_flow_nominal=func.get_data_property(subject,"massFlow.nominal",g,3)
medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
signalpath.status=func.get_data_property(instance,"signalpath.status",g,None)
signalpath.temperature=func.get_data_property(instance,"signalpath.temperature",g,None)
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
%>
AixLib.Fluid.BoilerCHP.CHP Combined_Heat_Power${number}(
	redeclare package Medium =${medium},
	param=AixLib.DataBase.CHP.CHP_FMB_1500_GSMK(),
	TSetIn=true,
	minCapacity=20,
    delayTime=300,
    m_flow_nominal=${m_flow_nominal})
	"${instance}"
    annotation (Placement(transformation(extent={${lu},${ro}})));
	
% if signalpath.status==None:		
Modelica.Blocks.Sources.BooleanConstant on${number}
    "CHP is always on"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));
% else:	
<%func.add_combitimetable(instance,instancedic,number,'on',signalpath.status,1)%>
<%func.real_to_boolean(instance,instancedic,'onBoolean',number,2)%>	
% endif					

% if signalpath.temperature==None:	
Modelica.Blocks.Sources.Constant TSet${number}(k=80 + 273.15)
    "Set temperature"
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][3]['position'][0]},${instancedic[instance]['add'][3]['position'][1]}})));
% else:	
<%func.add_combitimetable(instance,instancedic,number,'TSet',signalpath.temperature,3)%>		
% endif					

