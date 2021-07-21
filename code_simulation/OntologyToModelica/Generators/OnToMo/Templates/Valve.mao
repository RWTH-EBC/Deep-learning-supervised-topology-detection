<%page args="instance,instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
number=instancedic[instance]['number']
signalpath.position=func.get_data_property(instance,"signalpath.position",g,None)
%>
% if ('DIV'in instance)or('MX'in instance):
  <%
  subject=instance+"_PH.PRIM"
  m_flow_nominal=func.get_data_property(subject,"massFlow.nominal",g,6.5)
  dpValve_nominal=func.get_data_property(subject,"pressureDifference.nominal",g,10000)
  medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
  %>
AixLib.Fluid.Actuators.Valves.ThreeWayLinear Valve${number}(
	redeclare package Medium = ${medium},
	l={0.05,0.05},
	m_flow_nominal=${m_flow_nominal},
	use_inputFilter=false,
	dpValve_nominal=${dpValve_nominal},
	energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial)
	"${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));
	% if signalpath.position==None:
Modelica.Blocks.Sources.Constant position${number}(
	 k=0.7 ) "Control signal ${instance}"
	 annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));	
	 % else:
	<%func.add_combitimetable(instance,instancedic,number,'position',signalpath.position,1)%>
	% endif
% else:
<%
subject=instance+"_PH"
medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
%>
AixLib.Fluid.Actuators.Valves.SimpleValve Valve${number}(
	redeclare package Medium =${medium},
	m_flow_small=1e-4)
	"${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));
	% if signalpath.position==None:
Modelica.Blocks.Sources.Step position${number}(
    startTime=12000,
    height=0.5,
    offset=0.2)
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][1]['position'][0]},${instancedic[instance]['add'][1]['position'][1]}})));
	% else:
	<%func.add_combitimetable(instance,instancedic,number,'position',signalpath.position,1)%>
	% endif
% endif 


