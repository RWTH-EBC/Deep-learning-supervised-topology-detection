<%page args="boundarydic,n,g"/>
<%namespace name="func" file="function.mao" />
<%
instance=boundarydic['source'][n]['feeds']
lu=boundarydic['source'][n]['position'][0]
ro=boundarydic['source'][n]['position'][1]
medium=func.get_data_property(instance,"medium",g,"AixLib.Media.Specialized.Water.TemperatureDependentDensity")
m_flow=func.get_data_property(instance,"massFlow.nominal",g,"3")
%>
% if boundarydic['source'][n]['type']:
AixLib.Fluid.Sources.Boundary_pT source${n} (
	nPorts=1, 
	% if boundarydic['source'][n]['t']!={}:
	use_T_in=true,
	% endif	
	redeclare package Medium =${medium})
	"source feed ${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));
% else:		
Modelica.Fluid.Sources.MassFlowSource_T source${n}(
    nPorts=1,
	% if boundarydic['source'][n]['m']!={}:	
    use_m_flow_in=true, 
	% else:	
	m_flow=${m_flow},
	% endif	
	% if boundarydic['source'][n]['t']!={}:	
    use_T_in=true,
	% endif		
	redeclare package Medium =${medium})
	"source feed ${instance}"
	annotation (Placement(transformation(extent={${lu},${ro}})));
% endif		

% if boundarydic['source'][n]['t']!={}:
Modelica.Blocks.Sources.CombiTimeTable boundarytemperature${n}(
	smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
	extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
	tableOnFile=true,
	verboseRead=false,
	tableName="data",
	columns=1:1,
	offset={0,0},
	fileName=${boundarydic['source'][n]['t']['path']})
	    annotation (Placement(transformation(extent={${boundarydic['source'][n]['t']['position'][0]},${boundarydic['source'][n]['t']['position'][1]}})));
% endif	
% if boundarydic['source'][n]['m']!={} and not(boundarydic['source'][n]['type']):
Modelica.Blocks.Sources.CombiTimeTable boundarymassflow${n}(
	smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
	extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
	tableOnFile=true,
	verboseRead=false,
	tableName="data",
	columns=1:2,
	offset={0,0},
	fileName=${boundarydic['source'][n]['m']['path']})
	    annotation (Placement(transformation(extent={${boundarydic['source'][n]['m']['position'][0]},${boundarydic['source'][n]['m']['position'][1]}})));
% endif	