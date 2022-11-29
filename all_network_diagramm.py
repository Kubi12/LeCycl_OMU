import networkx as nx
from random import randrange
import math
import os
import pandas as pd
from urllib.parse import urlparse
from bokeh.plotting import show, figure, from_networkx
from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend, Renderer, LegendItem
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral8, inferno, viridis, Spectral4


TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"


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
    #os.chdir(os.getcwd() + os.sep + 'Persona')
    frames = []
    figures = []
    website_color = {}
    figure_ = figure(
        title="Graph Layout Demonstration",
        x_range=(-2.1,2.1),
        y_range=(-2.1,2.1),
        height=1000,
        width=1500,
        tools=TOOLS,
        tooltips=[
            ("Info:", "@start"),
        ],
    )
    figure_.grid.grid_line_color = None

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
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
            )
            sources_targets = sources_targets.dropna()
            graph_nx = nx.DiGraph()
            for source in sources_targets['source'].drop_duplicates():
                graph_nx.add_node(source)
            for edge in sources_targets.itertuples():
                graph_nx.add_edge(edge.source, edge.target)

            graph = from_networkx(graph_nx, nx.spring_layout, scale=1.8, center=(0,0),)
            graph.name = file.split('.')[0]

            def get_random_hex():
                return hex(randrange(17, 255))[2:].upper()

            color_participent = f'#{get_random_hex()}{get_random_hex()}{get_random_hex()}'

            graph.node_renderer.glyph = Circle(size=15, fill_color=color_participent)
            graph.node_renderer.selection_glyph = Circle(size=15, fill_color=color_participent)
            graph.node_renderer.hover_glyph = Circle(size=25, fill_color=color_participent)

            graph.edge_renderer.glyph = MultiLine(line_color=color_participent, line_alpha=0.8, line_width=5)
            graph.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_alpha=1, line_width=5)
            graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

            graph.selection_policy = NodesAndLinkedEdges()
            graph.inspection_policy = EdgesAndLinkedNodes()

            figure_.renderers.append(graph)

    legend = Legend(
        items=[
            LegendItem(
                label=renderer.name,
                renderers=[renderer.node_renderer, renderer.edge_renderer],
                index=index,
            )
            for index, renderer in enumerate(figure_.renderers)
        ]
    )
    figure_.add_layout(legend, 'right')
    figure_.legend.click_policy = 'hide'
    figure_.legend.location = 'right'
    figure_.legend.orientation = 'vertical'
    figure_.legend.background_fill_alpha=.6
    figure_.output_backend = 'svg'
    show(figure_)
