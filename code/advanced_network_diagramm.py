from collections import Counter
from random import randrange
import networkx as nx
import os
import pandas as pd
from urllib.parse import urlparse
from bokeh.plotting import show, figure, from_networkx
from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend, Renderer, LegendItem, LabelSet, OpenHead
from bokeh.models import (Line, BoxSelectTool, Circle, EdgesAndLinkedNodes,
                          HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, Arrow)
from bokeh.palettes import Spectral8, inferno, viridis, Spectral4
from bokeh.layouts import grid

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append(
            (pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() / 60)
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc


if __name__ == "__main__":
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    os.chdir(os.getcwd() + os.sep + 'Persona')
    frames = []
    figures = []
    website_color = {}
    figures = []

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(
                get_network_location)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            visits = []
            sources_targets = []

            for index, item in enumerate(data_frame.itertuples()):
                if item == 0:
                    continue
                try:
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
                    if current_web_site and next_web_site:
                        visits.append(f'{current_web_site}>{next_web_site}')
                    sources_targets.append([
                        data_frame['Web_site'][index-1],
                        item.Web_site,
                        data_frame['time_spend'][index-1],
                    ])
                except KeyError:
                    pass

            number_visits = Counter(visits)
            sources_targets = pd.DataFrame(sources_targets)
            sources_targets = sources_targets.rename(
                columns={0: 'source', 1: 'target', 2: 'value', },
            )
            sources_targets = sources_targets.dropna()

            graph_nx = nx.DiGraph()

            for source in sources_targets['source'].drop_duplicates():
                graph_nx.add_node(source)

            for edge in sources_targets.itertuples():
                graph_nx.add_edge(edge.source, edge.target)

            figure_ = figure(
                title=f"Graph {file.split('.')[0]}",
                x_range=(-2.1, 2.1),
                y_range=(-2.1, 2.1),
                x_axis_location=None,
                y_axis_location=None,
                tools=TOOLS,
                tooltips=[
                    ("Info:", "$name"),
                ],
                width=1500,
                height=1000,
                toolbar_location="above",
                toolbar_sticky=False,
            )
            figure_.hover.anchor = 'center'
            figure_.hover.attachment = 'above'
            figure_.hover.point_policy = 'follow_mouse'
            figure_.hover.line_policy = 'next'
            figure_.grid.grid_line_color = None
            graph_data_frame = pd.DataFrame(
                nx.spring_layout(graph_nx, scale=2))

            def get_random_hex():
                return hex(randrange(17, 255))[2:].upper()

            for source_name, target_name in graph_nx.edges:
                source = graph_data_frame[source_name]
                target = graph_data_frame[target_name]
                figure_.line(
                    [source[0], target[0]],
                    [source[1], target[1]],
                    line_color='black',
                    line_width=2.5,
                    line_alpha=.4,
                    name=f'{source_name}>{target_name}',
                )

            for website in graph_data_frame:
                figure_.circle(
                    x=graph_data_frame[website][0],
                    y=graph_data_frame[website][1],
                    name=website,
                    size=20,
                    fill_color=f'#{get_random_hex()}{get_random_hex()}{get_random_hex()}',
                )

            renderer_groups = {}
            for renderer in figure_.renderers:
                if '>' in renderer.name:
                    source, target = renderer.name.split('>')
                    try:
                        renderer_groups[source].append(renderer)
                        renderer_groups[target].append(renderer)
                    except KeyError as e:
                        renderer_groups[source] = [renderer]
                else:
                    try:
                        renderer_groups[renderer.name].append(renderer)
                    except KeyError as e:
                        renderer_groups[renderer.name] = [renderer]

            legend = Legend(
                items=[
                    LegendItem(
                        label=f'{key}',
                        renderers=value,
                        index=index,
                    )
                    for key, value in renderer_groups.items()
                ]
            )
            figure_.add_layout(legend, 'right')
            figure_.legend.click_policy = 'hide'
            figure_.legend.location = 'right'
            figure_.legend.orientation = 'vertical'
            figure_.legend.background_fill_alpha = .6
            figure_.output_backend = 'svg'
            figures.append(figure_)

    grid = grid(figures, nrows=3)
    show(grid)
