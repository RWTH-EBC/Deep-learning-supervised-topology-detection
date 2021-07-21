<%def name="initialize_position()">
<%
 pos={}
 lux=-120
 luy=80
 rox=-100
 roy=100
%>
% for i in range(0,20):
    <%
	 luy=luy-30
	 roy=roy-30
	 lux=-120
	 rox=-100
	%>
    % for j in range (1,6):
	  <%
	   p=i*5+j
	   lux=lux+40
	   rox=rox+40
	   pos[p]={}
	   pos[p]['model']=['{'+str(lux)+','+str(luy)+'}','{'+str(rox)+','+str(roy)+'}']
	   pos[p]['port']=['{'+str(lux)+','+str(luy+10)+'}','{'+str(rox)+','+str(roy-10)+'}']
	   pos[p]['3port']=['{'+str(lux)+','+str(luy+10)+'}','{'+str(rox)+','+str(roy-10)+'}','{'+str(rox-10)+','+str(roy)+'}','{'+str(rox-10)+','+str(roy)+'}']
	   pos[p]['4port']=['{'+str(lux)+','+str(luy+16)+'}','{'+str(rox)+','+str(roy-4)+'}','{'+str(rox)+','+str(roy-16)+'}','{'+str(lux)+','+str(luy+4)+'}']
	  %>
	% endfor 
% endfor 
<%return pos %>
</%def>


<%def name="add_source(pos,boundarydic,i,g)">
<%
n=0
boundarydic['source']={}
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
rows = g.query("""SELECT ?s WHERE {?m bf:hasPart ?s. MINUS {?s bf:isFedBy ?n.}}""")
m = {'http://example.com':'',}
res = [[m[r.split('#')[0]]+ r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
%>
% for equipment in res: 
	% for item in equipment:
		<%
		i=i+1
		n=n+1
		boundarydic['source'][n]={}
		boundarydic['source'][n]['position']=pos[i]['model']
		boundarydic['source'][n]['posport']=pos[i]['port']
		boundarydic['source'][n]['feeds']=item
		boundarydic['source'][n]['type']=g.query("""ASK{?s rdf:type brick:Pump.?s bf:hasPart ?o. {ex:%s bf:feeds*  ?o.}union{ex:%s bf:isFedBy*  ?o.}}""" %(item,item))
		%>
		% for property,condition in zip(["boundarypath.temperature","boundarypath.massflow"],["t","m"]):
			<%
			path=get_data_property(item,property,g,"None")
			boundarydic['source'][n][condition]={}
			%>
			% if path!="None":
				<%
				i=i+1
				boundarydic['source'][n][condition]['path']=path
				boundarydic['source'][n][condition]['position']=pos[i]['model']
				boundarydic['source'][n][condition]['posport']=pos[i]['port']
				%>
			% endif
		% endfor	
		<%include file="source.mao"  args="boundarydic=boundarydic,n=n,g=g"/>
	% endfor
% endfor
<%return boundarydic,i %>
</%def>


<%def name="add_sink(pos,boundarydic,i,g)">
<%
n=0
boundarydic['sink']={}
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
rows = g.query("""SELECT ?s WHERE {?m bf:hasPart ?s. MINUS {?s bf:feeds ?n.}}""")
m = {'http://example.com':'',}
res = [[m[r.split('#')[0]]+ r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
%>
% for equipment in res: 
	% for item in equipment:
		<%
		i=i+1
		n=n+1
		boundarydic['sink'][n]={}
		boundarydic['sink'][n]['position']=pos[i]['model']
		boundarydic['sink'][n]['posport']=pos[i]['port'][1]
		boundarydic['sink'][n]['isFedBy']=item
		%>	
		<%include file="sink.mao"  args="boundarydic=boundarydic,n=n,g=g"/>
	% endfor
% endfor
<%return boundarydic,i %>
</%def>


<%def name="instance_to_model(d,filename,pos,modelicamap,i,modelicamapadd,g)">
<%
instancedic={}
count={}
%>
% for ontology in ['BRICK','BUDO']:
    <%list=d[str(filename)][str(ontology)].keys()%>
    % for key in list:
		<%count[key]=0%>
        % for a in d[str(filename)][str(ontology)][str(key)]:		    
            % for b in a:
               % for instance in b:
					<%
					i=i+1
					instancedic[instance]={}
					instancedic[instance]['feeds']={}
					instancedic[instance]['hasPoint']={}
					count[key]=count[key]+1
					instancedic[instance]['key']=key
					instancedic[instance]['modelica']=str(modelicamap[key])+str(count[key])
					instancedic[instance]['position']=pos[i]['model']
					instancedic[instance]['number']=count[key]
					%>	
                    %  if (instancedic[instance]['key']in ['TP','VAL']) and (('DIV'in instance)or('MX'in instance)):
						<%
						instancedic[instance]['posport']=pos[i]['3port']
						instancedic[instance]['port_a1']=str(modelicamap[key])+str(count[key])+'.port_1'
						instancedic[instance]['port_b1']=str(modelicamap[key])+str(count[key])+'.port_2'		
						instancedic[instance]['port_a2']=str(modelicamap[key])+str(count[key])+'.port_3'
						instancedic[instance]['port_b2']=str(modelicamap[key])+str(count[key])+'.port_3'
						instancedic[instance]['feeds']['PH.PRIM']={}
						instancedic[instance]['feeds']['PH.SEC']={}
						instancedic[instance]['hasPoint']['PH.PRIM']=[]
						instancedic[instance]['hasPoint']['PH.SEC']=[]

						%>
					% elif (instancedic[instance]['key']in ['HP','HX']):
						<%
						instancedic[instance]['posport']=pos[i]['4port']
						instancedic[instance]['port_a1']=str(modelicamap[key])+str(count[key])+'.port_a1'
						instancedic[instance]['port_b1']=str(modelicamap[key])+str(count[key])+'.port_b1'		
						instancedic[instance]['port_a2']=str(modelicamap[key])+str(count[key])+'.port_a2'
						instancedic[instance]['port_b2']=str(modelicamap[key])+str(count[key])+'.port_b2'
						instancedic[instance]['feeds']['PH.PRIM']={}
						instancedic[instance]['feeds']['PH.SEC']={}						
						instancedic[instance]['hasPoint']['PH.PRIM']=[]
						instancedic[instance]['hasPoint']['PH.SEC']=[]
						%>					
					% elif (instancedic[instance]['key']in ['T.MEA']):
					    <%
						instancedic[instance]['posport']=pos[i]['port']
						instancedic[instance]['port_a1']=str(modelicamap[key])+str(count[key])+'.port_a'
						instancedic[instance]['port_b1']=str(modelicamap[key])+str(count[key])+'.port_b'
						instancedic[instance]['feeds']={}
						instancedic[instance]['hasPoint']={}						
						%>

					% else:
						<%
						instancedic[instance]['posport']=pos[i]['port']
						instancedic[instance]['port_a1']=str(modelicamap[key])+str(count[key])+'.port_a'
						instancedic[instance]['port_b1']=str(modelicamap[key])+str(count[key])+'.port_b'
						instancedic[instance]['feeds']['PH']={}						
						instancedic[instance]['hasPoint']['PH']=[]
						%>
					% endif
					% if key in modelicamapadd:
						<%instancedic[instance]['add']={}%>
						% for c in range (1,modelicamapadd[key]+1):
						    <%
							i=i+1
							instancedic[instance]['add'][c]={}
							instancedic[instance]['add'][c]['position']=pos[i]['model']
							instancedic[instance]['add'][c]['posport']=pos[i]['port']
							%>
						% endfor
					%endif	  
					<%include file="${modelicamap[key]}.mao" args="instance=instance,instancedic=instancedic,g=g"/>	
			   % endfor
 		    % endfor
        % endfor
    % endfor
% endfor
<%return instancedic, i, count %>
</%def>


<%def name="generate_pipe(g,pos,i,instancedic)">
<%
pipedic={}
pipe=0
%>
<%list=instancedic.keys()%>	
% for instance in list:		
	% for portHeat in instancedic[instance]['feeds'].keys():
		<%
		port_instance=instance+'_'+portHeat		
		res=get_instance(port_instance,"feeds",g)
		%>
		% for equipment in res:
			   % for item in equipment:
						% if '_'.join(item.split('_')[0:-1])!=instance:
							<%						
							i=i+1
							pipe=pipe+1
							pipedic[pipe]={}
							pipedic[pipe]['position']=pos[i]['model']
							pipedic[pipe]['posport']=pos[i]['port']
							instancedic[instance]['feeds'][portHeat][item]=pipe
							%>
							<%include file="pipe.mao" args="port_instance=port_instance,item=item,pipe=pipe,pipedic=pipedic,g=g"/>
						% endif						 								  
			   % endfor
		% endfor
	% endfor	
% endfor
<%return instancedic, pipedic, i %>
</%def>

<%def name="get_sensor_point(g,instancedic)">
<%list=instancedic.keys()%>	
% for instance in list:		
	% for portHeat in instancedic[instance]['hasPoint'].keys():
		<%
		port_instance=instance+'_'+portHeat		
		res=get_instance(port_instance,"hasPoint",g)
		%>
		% for point in res:
		   % for item in point:
				% if item in list:
					<%instancedic[instance]['hasPoint'][portHeat].append(item)%>
				% endif								  
		   % endfor
		% endfor	
	% endfor
% endfor	
<%return instancedic %>
</%def>



<%def name="get_feeds_relationship(g,instancedic)">
<%list=instancedic.keys()%>	
% for instance in list:		
	% for portHeat in instancedic[instance]['feeds'].keys():
		<%
		port_instance=instance+'_'+portHeat		
		res=get_instance(port_instance,"feeds",g)
		%>
		% for equipment in res:
			   % for item in equipment:
						% if '_'.join(item.split('_')[0:-1])!=instance:
							<%instancedic[instance]['feeds'][portHeat][item]=1%>
						% endif						 								  
			   % endfor
		% endfor
	% endfor	
% endfor
<%return instancedic %>
</%def>



<%def name="connect_control_signal(instancedic,modelicamapadd,modelicamap,g)">
<%list=instancedic.keys()%>	
% for instance in list:	
	% if instancedic[instance]['key']in modelicamapadd:
	 <%include file="${modelicamap[instancedic[instance]['key']]}_link.mao" args="instance=instance, instancedic=instancedic, g=g"/>
    % endif
% endfor 
</%def>

<%def name="connect_sensor_point(instancedic,g)">
<%list=instancedic.keys()%>	
<%port_map={'PH.PRIM':0,'PH.SEC':1,'PH':0}%>
% for instance in list:	
	% for portHeat in instancedic[instance]['hasPoint'].keys():		
		% for item in instancedic[instance]['hasPoint'][portHeat]:
			<%position=get_data_property(item,"position",g,"out")%>
			<%r=port_map[portHeat]%>
			% if position=="out":
connect(${instancedic[instance]['port_b'+str(r+1)]}, ${instancedic[item]['port_a1']})
	annotation (Line(points={${instancedic[instance]['posport'][2*r+1]},${instancedic[item]['posport'][0]}}, color={0,127,255}));
				 <%
				 instancedic[instance]['posport'][1]=instancedic[item]['posport'][1]
				 instancedic[instance]['port_b'+str(r+1)]=instancedic[item]['port_b1']
				 %>
			% else: 
connect(${instancedic[instance]['port_a'+str(r+1)]}, ${instancedic[item]['port_b1']})
	annotation (Line(points={${instancedic[instance]['posport'][2*r]},${instancedic[item]['posport'][1]}}, color={0,127,255}));
				 <%
				 instancedic[instance]['posport'][0]=instancedic[item]['posport'][0]
				 instancedic[instance]['port_a'+str(r+1)]=instancedic[item]['port_a1']
				 %>
			% endif			
		% endfor
	% endfor        
% endfor  
<%return instancedic %>
</%def>

<%def name="connect_model_with_pipe(instancedic,pipedic)">
<%list=instancedic.keys()%>	
<%port_map={'PH.PRIM':0,'PH.SEC':1,'PH':0}%>
% for instance in list:
	% for portHeat in instancedic[instance]['feeds'].keys():		
		% for port_item in instancedic[instance]['feeds'][portHeat]:
			<%
			np=instancedic[instance]['feeds'][portHeat][port_item]
			item='_'.join(port_item.split('_')[0:-1])
			r=port_map[portHeat]
			j=port_map[port_item.split('_')[-1]]
			%>
connect(${instancedic[instance]['port_b'+str(r+1)]}, pipe${np}.port_a)
	annotation (Line(points={${instancedic[instance]['posport'][2*r+1]},${pipedic[np]['posport'][0]}}, color={0,127,255}));
connect(pipe${np}.port_b, ${instancedic[item]['port_a'+str(j+1)]})
	annotation (Line(points={${pipedic[np]['posport'][1]},${instancedic[item]['posport'][2*j]}}, color={0,127,255}));
		% endfor
	% endfor        
% endfor  
</%def>

<%def name="connect_model_without_pipe(instancedic)">
<%list=instancedic.keys()%>	
<%port_map={'PH.PRIM':0,'PH.SEC':1,'PH':0}%>
% for instance in list:
	% for portHeat in instancedic[instance]['feeds'].keys():		
		% for port_item in instancedic[instance]['feeds'][portHeat]:
			<%
			item='_'.join(port_item.split('_')[0:-1])
			r=port_map[portHeat]
			j=port_map[port_item.split('_')[-1]]
			%>
connect(${instancedic[instance]['port_b'+str(r+1)]}, ${instancedic[item]['port_a'+str(j+1)]})
	annotation (Line(points={${instancedic[instance]['posport'][2*r+1]},${instancedic[item]['posport'][2*j]}}, color={0,127,255}));
		% endfor
	% endfor        
% endfor  
</%def>


<%def name="connect_source_and_sink(instancedic,boundarydic)">
<%port_map={'PH.PRIM':0,'PH.SEC':1,'PH':0}%>
% for n in boundarydic['source'].keys():
	<%j=port_map[boundarydic['source'][n]['feeds'].split('_')[-1]]%>
	<%item='_'.join(boundarydic['source'][n]['feeds'].split('_')[0:-1])%>				
connect(source${n}.ports[1],${instancedic[item]['port_a'+str(j+1)]})
	annotation (Line(points={${boundarydic['source'][n]['posport'][1]},${instancedic[item]['posport'][2*j]}}, color={0,127,255}));
	% if boundarydic['source'][n]['t']!={}:
connect(boundarytemperature${n}.y[2], source${n}.T_in) 
	annotation (Line(points={${boundarydic['source'][n]['t']['posport'][1]},${boundarydic['source'][n]['posport'][0]}}, color={0,0,127}));	
	% endif
	% if boundarydic['source'][n]['m']!={} and not(boundarydic['source'][n]['type']):
connect(boundarymassflow${n}.y[2], source${n}.m_flow_in) 
	annotation (Line(points={${boundarydic['source'][n]['m']['posport'][1]},${boundarydic['source'][n]['posport'][0]}}, color={0,0,127}));
	% endif
% endfor 
% for n in boundarydic['sink'].keys():
	<%j=port_map[ boundarydic['sink'][n]['isFedBy'].split('_')[-1]]%>
	<%item='_'.join(boundarydic['sink'][n]['isFedBy'].split('_')[0:-1])%>		
connect(${instancedic[item]['port_b'+str(j+1)]},sink${n}.ports[1])
	annotation (Line(points={${instancedic[item]['posport'][2*j+1]},${boundarydic['sink'][n]['posport']}}, color={0,127,255}));      
% endfor   	
<%return boundarydic %>
</%def>


<%def name="get_data_property(instance,property,g,initial)">
<%from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal%>
% if property=="medium":
	% if "PH"in instance:
		<%rows = g.query("""SELECT ?m WHERE{  { ex:%s bf:feeds*  ?o.}union{  ex:%s bf:isFedBy* ?o.}union {{  ex:%s bf:feeds*  ?e.}union{  ex:%s bf:isFedBy* ?e.} ?e bf:hasPoint ?o.}?o budo:medium ?m.} """ %(instance,instance,instance,instance))%>
	% else:
		<%rows = g.query("""SELECT ?m WHERE{ ex:%s bf:isPointOf ?a.  {?a bf:feeds*  ?o.}union{ ?a bf:isFedBy* ?o.}union {{ ?a bf:feeds*  ?e.}union{ ?a bf:isFedBy* ?e.} ?e bf:hasPoint ?o.}?o budo:medium ?m.} """ %(instance))%>
	% endif	
% else:		
	<%rows = g.query("""SELECT ?o WHERE {ex:%s budo:%s ?o .}""" % (instance,property))%>
% endif		
<%res = [[r.split('(')[-1] for r in row] for row in rows]%>
% if len(res)==0:
	<%parameter=initial%>
% else:
	<%parameter=res[0][0]%>
% endif
<%return parameter%>
</%def>


<%def name="get_instance(instance,relationship,g)">
<%
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
rows = g.query("""SELECT ?o WHERE {ex:%s bf:%s ?o .}""" % (instance,relationship))
m = {'http://example.com':'',}
res = [[m[r.split('#')[0]]+ r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
return res
%>
</%def>

<%def name="add_combitimetable(instance,instancedic,number,name,filepath,npos)">
Modelica.Blocks.Sources.CombiTimeTable ${name}${number}(
	smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
	extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
	tableOnFile=true,
	verboseRead=false,
	tableName="data",
	columns=1:1,
	offset={0,0},
	fileName=${filepath})
	annotation (Placement(transformation(extent={${instancedic[instance]['add'][npos]['position'][0]},${instancedic[instance]['add'][npos]['position'][1]}})));	
</%def>

<%def name="real_to_boolean(instance,instancedic,name,number,npos)">
 Modelica.Blocks.Math.RealToBoolean ${name}${number}
    annotation (Placement(transformation(extent={${instancedic[instance]['add'][npos]['position'][0]},${instancedic[instance]['add'][npos]['position'][1]}})));	
</%def>



