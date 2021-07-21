<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject=instance+"_portHeatflow"
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
number=instancedic[instance]['number']
m_flow_nominal=func.get_data_property(subject,"massFlow.nominal",g,3)
medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
signalpath.massflow=func.get_data_property(instance,"signalpath.massflow",g,None)
%>
AixLib.Fluid.Movers.FlowControlled_m_flow Pump${number}(
	m_flow_nominal=${m_flow_nominal},
	redeclare 
	AixLib.Fluid.Movers.Data.Pumps.Wilo.VeroLine80slash115dash2comma2slash2
	per,
	redeclare package Medium =${medium},
	each allowFlowReversal=false,
	energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial)
	"${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));
	
% if signalpath.massflow==None:	
Modelica.Blocks.Sources.Pulse pulse${number}(
	width=50,
    offset=1,
    period=1000)
	annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));
% else:
<%func.add_combitimetable(instance,instancedic,number,'massflow',signalpath.massflow,1)%>
% endif
