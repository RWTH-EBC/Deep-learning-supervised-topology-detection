<%namespace name="func" file="function.mao" />
<% 
from rdflib import RDFS, RDF, Namespace, Graph, URIRef, Literal
g=d['Graph']
g_str = g.serialize(format='turtle').decode('utf-8')
path_brick=d['path_brick']
path_budo=d['path_budo']
%>
${g_str}
<%func.visualization(g,path_brick,path_budo)%>

