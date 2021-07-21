<%def name="query_result(rows)">
<%
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
m = {
	'https://brickschema.org/schema/1.0.3/Brick': 'brick',
	'http://www.w3.org/1999/02/22-rdf-syntax-ns': 'rdf',
	'http://www.w3.org/2000/01/rdf-schema': 'rdfs',
	'https://brickschema.org/schema/1.0.3/BrickFrame': 'bf',
	'http://www.w3.org/2002/07/owl': 'owl',
	'http://www.w3.org/2004/02/skos/core': 'skos',
	'http://example.com': 'ex',
	'https://git.rwth-aachen.de/EBC/Team_BA/misc/Machine-Learning/tree/MA_fst-bll/building_ml_platform/BUDO-M/Platform_Application_AI_Buildings_MA_Llopis/OntologyToModelica/CoTeTo/ebc_jsonld':'budo'
	}
res = [[m[r.split('#')[0]] + ':' + r.split('#')[1] if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows]
return res
%>
</%def>


<%def name="visualization(g,path_brick,path_budo)">
<%
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
import networkx as nx
import matplotlib.pyplot as plt
import os
q1 = """select ?s ?p ?o where {?s ?p ?o .}"""
q2 = """select ?s where {?o rdfs:subClassOf* brick:Point. ?s rdf:type ?o}"""
q3 = """select ?s where {{?o rdfs:subClassOf* brick:Equipment. ?s rdf:type ?o} UNION{?o rdfs:subClassOf* budo:pipeFitting. ?s rdf:type ?o}} """
q4 = """select ?s where {?o rdfs:subClassOf* brick:Location. ?s rdf:type ?o}"""
q5 = """select ?s where {?o rdfs:subClassOf* budo:Port. ?s rdf:type ?o}"""
rows = g.query(q1)
res=query_result(rows)
G = nx.DiGraph()    
for row in res:
	if 'ex' in row[2]:
		G.add_edge(row[0], row[2],predicate=row[1]) 
g.parse(path_brick, format='turtle') 
g.parse(path_budo, format='turtle')
query_list=[q2,q3,q4,q5]
color_choice=['green','red','yellow','black']
i=0
for q in query_list:        
	rows = g.query(q)
	res=query_result(rows)
	for row in res:   
		G.node[row[0]]['color'] = color_choice[i]
	i=i+1
colors=[]
for node,attribute in tuple (G.nodes(data=True)):  
	if 'color'in attribute:
		colors.append(attribute['color'])
	else:
		colors.append('pink')
nx.draw(G,pos=nx.spring_layout(G),with_labels=True, edge_color='b',node_size=600, node_color = colors,arrows=True,width=0.3,font_family='sans-serif', alpha=0.5, font_size=8)        
plt.show()
%>
</%def>

