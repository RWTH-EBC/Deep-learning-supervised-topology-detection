<%page args="instance, instancedic,g"/>
<%namespace name="func" file="function.mao" />
<%
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.loadratio=func.get_data_property(instance,"signalpath.loadratio",g,None)
%>	
% if signalpath.loadratio==None:					
connect(uCom${number}.y,Heat_Pump${number}. y) 
	annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}}, color={0,0,127},smooth=Smooth.None));
% else:
connect(uCom${number}.y[2],Heat_Pump${number}. y) 
		annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}}, color={0,0,127}, smooth=Smooth.None));
% endif					



