<%namespace name="func" file="function.mao" />
within ;
% for filename, content in d.items():
   <%name=d[filename]["outputfile_name"]%>
model ${name}
% endfor
<%
from rdflib import Graph
g = Graph()
g.parse(filename, format='turtle')
haspipe=d[str(filename)]['pipe']
modelicamap=d[str(filename)]['modelica_map']
modelicamapadd=d[str(filename)]['modelica_additional_model_number']
pos=func.initialize_position()
boundarydic={}
i=0
%>

inner Modelica.Fluid.System system
	annotation (Placement(transformation(extent={{-100,80},{-80,100}})));	

<%(boundarydic,i)=func.add_source(pos,boundarydic,i,g)%>	
<%(instancedic,i,count)=func.instance_to_model(d,filename,pos,modelicamap,i,modelicamapadd,g)%>
% if haspipe=='No':
	<%instancedic=func.get_feeds_relationship(g,instancedic)%>
% else:
	<%(instancedic,pipedic,i)=func.generate_pipe(g,pos,i,instancedic)%>	
% endif
<%instancedic=func.get_sensor_point(g,instancedic)%>	
<%(boundarydic,i)=func.add_sink(pos,boundarydic,i,g)%>				

equation
<%func.connect_control_signal(instancedic,modelicamapadd,modelicamap,g)%>	
<%instancedic=func.connect_sensor_point(instancedic,g)%>
% if haspipe=='No':
	<%func.connect_model_without_pipe(instancedic)%>
% else:
	<%func.connect_model_with_pipe(instancedic,pipedic)%>
% endif	    
<%boundarydic=func.connect_source_and_sink(instancedic,boundarydic)%>							
	annotation (uses(AixLib(version="0.5.2"), Modelica(version="3.2.2")));
end ${name};
<%
###print(count)
###print(instancedic)
###print(pipedic)
###print(boundarydic)
###print(pos)
###print(modelicamap)
###print(modelicamapadd)
%>
