<%page args="port_instance,item,pipe,pipedic,g"/>
<%namespace name="func" file="function.mao" />
<%
lu=pipedic[pipe]['position'][0]
ro=pipedic[pipe]['position'][1]
diameter=func.get_data_property(port_instance,"diameterPipe.out",g,0.05)
length=func.get_data_property(port_instance,"lengthPipe.out",g,3)
m_flow_nominal=func.get_data_property(port_instance,"massFlow.nominal.Pipe.out",g,3)
dp_nominal=func.get_data_property(port_instance,"pressureDifference.nominal.Pipe.out",g,2500)
medium=func.get_data_property(port_instance,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
%>
AixLib.Fluid.FixedResistances.PressureDrop pipe${pipe}(
	m_flow_nominal=${m_flow_nominal},
	each dp_nominal=${dp_nominal},
	each allowFlowReversal=false,
	redeclare package Medium =${medium})
	"${port_instance} feeds ${item}"	 
	annotation (Placement(transformation(extent={${lu},${ro}})));