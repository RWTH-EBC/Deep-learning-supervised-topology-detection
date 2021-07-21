<%page args="instance,instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
number=instancedic[instance]['number']
medium=func.get_data_property(instance,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
m_flow_nominal=func.get_data_property(instance,"massFlow.nominal",g,3)
%>
AixLib.Fluid.Sensors.TemperatureTwoPort Temperature_Sensor${number}(
	redeclare package Medium = ${medium},
	m_flow_nominal=${m_flow_nominal},tau=0) 
	"${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));