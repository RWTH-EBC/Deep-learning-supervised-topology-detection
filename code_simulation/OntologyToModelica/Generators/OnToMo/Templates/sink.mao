<%page args="boundarydic,n,g"/>
<%namespace name="func" file="function.mao" />
<%
instance=boundarydic['sink'][n]['isFedBy']
lu=boundarydic['sink'][n]['position'][0]
ro=boundarydic['sink'][n]['position'][1]
medium=func.get_data_property(instance,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
%>
Modelica.Fluid.Sources.Boundary_pT sink${n} 
	(nPorts=1, redeclare package Medium =${medium})
	"sink isFedby ${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));