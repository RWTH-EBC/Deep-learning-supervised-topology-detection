<%page args="instance, instancedic, g"/>
<%namespace name="func" file="function.mao" />
<%
number=instancedic[instance]['number']
lu=instancedic[instance]['position'][0]
ro=instancedic[instance]['position'][1]
signalpath.position=func.get_data_property(instance,"signalpath.position",g,None)
%>
% if signalpath.position==None:
	% if ('DIV'in instance)or('MX'in instance):
	connect(position${number}.y, Valve${number}.y) 
		annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}},color={0,0,127}));	
	% else:
	connect(position${number}.y, Valve${number}.opening) 
		annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}},color={0,0,127}));				
	% endif 
% else:
	% if ('DIV'in instance)or('MX'in instance):
	connect(position${number}.y[2], Valve${number}.y) 
		annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}},color={0,0,127}));	
	% else:
	connect(position${number}.y[2], Valve${number}.opening) 
		annotation (Line(points={${instancedic[instance]['add'][1]['posport'][1]},${ro}},color={0,0,127}));				
	% endif 
% endif 	