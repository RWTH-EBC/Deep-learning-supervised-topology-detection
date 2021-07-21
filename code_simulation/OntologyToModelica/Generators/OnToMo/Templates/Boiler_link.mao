<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.status=func.get_data_property(instance,"signalpath.status",g,None)
signalpath.temperature=func.get_data_property(instance,"signalpath.temperature",g,None)
signalpath.mode=func.get_data_property(instance,"signalpath.mode",g,None)
%>
% if signalpath.status==None:	
connect(isOn${number}.y, Boiler${number}.isOn)
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${lu}}, color={255,0,255}));
% else:
connect(isOn${number}.y[2],  isOnBoolean${number}.u)
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${instancedic[instance]['add'][2]['posport'][0]}}, color={0,0,127}));
connect(isOnBoolean${number}.y, Boiler${number}.isOn)
	annotation (Line(points={${instancedic[instance]['add'][2]['posport'][1]},${lu}}, color={255,0,255}));	
% endif
% if signalpath.temperature==None:
connect(TAmbient${number}.y, Boiler${number}.TAmbient) 
	annotation (Line(points={${instancedic[instance]['add'][3]['posport'][1]},${ro}}, color={0,0,127}));
% else:	
connect(TAmbient${number}.y[2], Boiler${number}.TAmbient) 
	annotation (Line(points={${instancedic[instance]['add'][3]['posport'][1]},${ro}}, color={0,0,127}));	
% endif
% if signalpath.mode==None:		
connect(switchToNightMode${number}.y,Boiler${number}.switchToNightMode)  
	annotation (Line(points={${instancedic[instance]['add'][4]['posport'][1]},${lu}}, color={255,0,255}));					
% else:
connect(switchToNightMode${number}.y[2],  switchToNightModeBoolean${number}.u)
	annotation (Line(points={${instancedic[instance]['add'][4]['posport'][1]},${instancedic[instance]['add'][5]['posport'][0]}}, color={0,0,127}));
connect(switchToNightModeBoolean${number}.y, Boiler${number}.switchToNightMode)
	annotation (Line(points={${instancedic[instance]['add'][5]['posport'][1]},${lu}}, color={255,0,255}));		
% endif


