<%page args="instance,instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject=instance+"_PH.PRIM"
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
number=instancedic[instance]['number']
medium=func.get_data_property(subject,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
%>
Modelica.Fluid.Fittings.TeeJunctionIdeal T_Piece${number}(
	redeclare package Medium =${medium})
	"${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));


