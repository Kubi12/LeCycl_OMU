# from matplotlib.sankey import Sankey
import networkx as nx
import math
import os
import pandas as pd
from urllib.parse import urlparse
# import holoviews as hv
# from holoviews import opts, dim
from bokeh.plotting import show, figure, from_networkx
from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
                                                    MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral8, inferno, viridis, Spectral4
# hv.extension('bokeh')


def reduce_(item, next):
    pass

# draw quadratic bezier paths
def bezier(start, end, control, steps):
        return [(1-s)**2*start + 2*(1-s)*s*control + s**2*end for s in steps]


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() / 60)
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc

if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    frames = []
    figures = []
    website_color = {}


    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            # renderer = hv.renderer('bokeh')
            sources_targets = []
            for index, item in enumerate(data_frame.itertuples()):
                if index == 0:
                    continue
                current_web_site, next_web_site = (
                    data_frame['Web_site'][index-1],
                    item.Web_site,
                )
                if current_web_site == next_web_site:
                    if sources_targets:
                        sources_targets[-1][-1] += float(
                            data_frame['time_spend'][index]
                        )
                        continue
                sources_targets.append([
                    data_frame['Web_site'][index-1],
                    item.Web_site,
                    data_frame['time_spend'][index-1],
                ])
            sources_targets = pd.DataFrame(sources_targets)
            sources_targets = sources_targets.rename(
                columns={0: 'source', 1: 'target', 2: 'value',},
            )# [:20]
            print(sources_targets)
            sources_targets = sources_targets.dropna()
            graph_nx = nx.DiGraph()
            for source in sources_targets['source'].drop_duplicates():
                graph_nx.add_node(source)
            for edge in sources_targets.itertuples():
                graph_nx.add_edge(edge.source, edge.target)
            plot = figure(
                title="Graph Layout Demonstration",
                x_range=(-2.1,2.1),
                y_range=(-2.1,2.1),
            )

            plot.grid.grid_line_color = None
            # graph = from_networkx(graph_nx, nx.random_layout, dim=2, seed=0, center=(0,0))
            graph = from_networkx(graph_nx, nx.spring_layout, scale=1.8, center=(0,0))
            graph.node_renderer.data_source.data['colors'] = viridis(len(graph_nx))
            graph.node_renderer.data_source.data['index'] = sources_targets['source'].drop_duplicates()

            graph.node_renderer.glyph = Circle(size=15, fill_color='colors')
            graph.node_renderer.glyph.name = 'NN'
            graph.node_renderer.selection_glyph = Circle(size=15, fill_color='colors')
            graph.node_renderer.hover_glyph = Circle(size=25, fill_color='colors')

            graph.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
            graph.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_alpha=1, line_width=5)
            graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

            graph.selection_policy = NodesAndLinkedEdges()
            # graph.inspection_policy = EdgesAndLinkedNodes()

            plot.renderers.append(graph)
            plot.add_tools(HoverTool(tooltips=[("source", "@index")]), TapTool(), BoxSelectTool())
            plot.add_layout(Legend(), 'right')

            show(plot)
            # sankey = hv.Sankey(sources_targets[:20])
            # sankey.opts(
            #     label_position='left',
            #     edge_color='target',
            #     node_color='index',
            #     cmap='tab20',
            # )
            # sankey.opts(width=600, height=400)
            # renderer.save(sankey, 'sankey.html')
            break


# – User action: The type of the user action. It can be one of the following:
# TabCreate, TabActivate, TabUpdate, TabRemove, ClipboardCopy, and WindowScroll.
# Start: Tabcreate
# second: Tabactivate, Tabupdate
# clipbord copy for new search?
# tabremove : finish
# https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0
