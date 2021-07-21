<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.status=func.get_data_property(instance,"signalpath.status",g,None)
signalpath.temperature=func.get_data_property(instance,"signalpath.temperature",g,None)
%>
% if signalpath.status==None:	
connect(on${number}.y, Combined_Heat_Power${number}.on)
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${lu}}, color={255,0,255}));
% else:
connect(on${number}.y[2],  onBoolean${number}.u)
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${instancedic[instance]['add'][2]['posport'][0]}}, color={0,0,127}));
connect(onBoolean${number}.y, Combined_Heat_Power${number}.on)
	annotation (Line(points={${instancedic[instance]['add'][2]['posport'][1]},${lu}}, color={255,0,255}));		
% endif					


% if signalpath.temperature==None:	
connect(TSet${number}.y, Combined_Heat_Power${number}.TSet) 
	annotation (Line(points={${instancedic[instance]['add'][3]['posport'][1]},${ro}}, color={0,0,127}));
% else:				
connect(TSet${number}.y[2], Combined_Heat_Power${number}.TSet) 
	annotation (Line(points={${instancedic[instance]['add'][3]['posport'][1]},${ro}}, color={0,0,127}));
% endif						



