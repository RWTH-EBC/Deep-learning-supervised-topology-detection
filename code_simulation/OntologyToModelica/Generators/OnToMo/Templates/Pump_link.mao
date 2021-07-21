<%page args="instance, instancedic, g"/>
<%namespace name="func" file="function.mao" />
<%
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.massflow=func.get_data_property(instance,"signalpath.massflow",g,None)
%>
% if signalpath.massflow==None:	
connect(pulse${number}.y, Pump${number}.m_flow_in)			
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${lu}}, color={0,0,127}));
% else:
connect(massflow${number}.y[2], Pump${number}.m_flow_in)
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${lu}}, color={0,0,127}));
% endif	