import json
import pandas as pd
from bokeh.plotting import from_networkx
from pandas import DataFrame
from pandas.io.json import json_normalize
import collections
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import hvplot.networkx as hvnx
import holoviews as hv
hv.extension('bokeh')
from bokeh.io import show, curdoc
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4

with open('C:/Users/Luciene/PycharmProjects/app/templates/package_dynamic_triagem_example.json', "r") as read_file:
 file_content = json.load(read_file)
data = json_normalize(file_content)
print(data)

rela = data.relationships
rela[0], type(rela[0])
column_names = rela[0][1].keys()
print(column_names)

values = [row.values() for row in rela[0]]
print(values)

new_df = pd.DataFrame(values,columns=column_names)
print(new_df)

plt.figure(figsize=(12, 12))

g2 = nx.from_pandas_edgelist(new_df, target='target_ref', source='source_ref') # 1. Create the graph
layout = nx.spring_layout(g2,iterations=50) # 2. Create a layout for our nodes

# 3. Draw the parts we want
nx.draw_networkx_edges(g2, layout, edge_color='#AAAAAA')
targets = [node for node in g2.nodes() if node in new_df.target_ref.unique()]
nx.draw_networkx_nodes(g2, layout, nodelist=targets, node_size=100, node_color='#AAAAAA')

sources = [node for node in g2.nodes() if node in new_df.source_ref.unique()]
size = [g2.degree(node) * 80 for node in g2.nodes() if node in new_df.source_ref.unique()]
nx.draw_networkx_nodes(g2, layout, nodelist=sources, node_size=size, node_color='lightblue')

high_degree_source = [node for node in g2.nodes() if node in new_df.source_ref.unique() and g2.degree(node) > 1]
nx.draw_networkx_nodes(g2, layout, nodelist=high_degree_source, node_size=100, node_color='#fc8d62')

targets_dict = dict(zip(targets, targets))
sources_dict = dict(zip(sources, sources))
nx.draw_networkx_labels(g2, layout, labels=targets_dict)
hvnx.draw(g2).opts(tools=[HoverTool(tooltips=[('target', '@index_hover')])])

plt.axis('off') # 4. Turn off the axis

plt.title("Dynamic Triagem Relationship") # 5. Tell matplotlib to show it
plt.show()

def create_graph(layout_func, inspection_policy=None, selection_policy=None, **kwargs):

    plot = Plot(plot_width=400, plot_height=400,
                x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
    graph_renderer = from_networkx(g2, layout_func, **kwargs)

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)
    # add meta data of start and end nodes to edge data source
    graph_renderer.edge_renderer.data_source.data['metadata'] = g2.edges()

    graph_renderer.inspection_policy = inspection_policy
    graph_renderer.selection_policy = selection_policy

    plot.renderers.append(graph_renderer)

    return plot


plot_3 = create_graph(layout, inspection_policy=EdgesAndLinkedNodes(), scale=2, center=(0,0))
plot_3.title.text = "Random Layout (EdgesAndLinkedNodes inspection policy)"
plot_3.add_tools(HoverTool(line_policy='interp', tooltips=[("(targets, sources)", "@metadata")]))

layout = plot_3

doc = curdoc()
doc.add_root(layout)

show(layout)

