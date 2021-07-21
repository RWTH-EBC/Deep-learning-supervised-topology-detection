<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
subject1=instance+"_PH.PRIM"
subject2=instance+"_PH.SEC"
m1_flow_nominal=float(func.get_data_property(subject1,"massFlow.nominal",g,3))
m2_flow_nominal=func.get_data_property(subject2,"massFlow.nominal",g,3)
medium1=func.get_data_property(subject1,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
medium2=func.get_data_property(subject2,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
dp1_nominal=func.get_data_property(subject1,"pressureDifference.nominal",g,10000)
dp2_nominal=func.get_data_property(subject2,"pressureDifference.nominal",g,10000)
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
%>
AixLib.Fluid.HeatExchangers.ConstantEffectiveness Heat_Exchanger${number}(
    redeclare package Medium1 = ${medium1},
    redeclare package Medium2 = ${medium2},
    show_T=true,
    m1_flow_nominal=${m1_flow_nominal},
    m2_flow_nominal=${m2_flow_nominal},
    dp1_nominal(displayUnit="Pa") = ${dp1_nominal},
    dp2_nominal(displayUnit="Pa") = ${dp2_nominal})
	"${instance}"
    annotation (Placement(transformation(extent={${lu},${ro}})));