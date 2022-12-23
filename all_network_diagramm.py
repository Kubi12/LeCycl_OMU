from post_survey_analysis import get_usefull_websites
from collections import Counter
import networkx as nx
import os
import pandas as pd
from bokeh.plotting import show, figure, from_networkx
from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend, Renderer, LegendItem
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral8, inferno, viridis, Spectral4


from utils import (
    calculate_time_spends,
    get_network_location,
    get_random_color,
)
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"


def add_websites_most_visited(file, most_visited, current_web_site, next_web_site):
    try:
        if current_web_site:
            most_visited[
                f'{file.split(".")[0]}'
            ].append(current_web_site)
    except KeyError:
        if current_web_site:
            most_visited[
                f'{file.split(".")[0]}'] = [current_web_site]
    try:
        if next_web_site:
            most_visited[
                f'{file.split(".")[0]}'].append(next_web_site)
    except KeyError:
        if next_web_site:
            most_visited[
                f'{file.split(".")[0]}'] = [next_web_site]


def get_sources_targets_for(file, visits, most_visited):
    data_frame = pd.read_csv(file)
    data_frame['Web_site'] = data_frame['Tab_URL'].apply(
        get_network_location
    )
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
        add_websites_most_visited(file, most_visited, current_web_site, next_web_site)
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
    sources_targets = pd.DataFrame(sources_targets)
    sources_targets = sources_targets.rename(
        columns={0: 'source', 1: 'target', 2: 'value',},
    )
    sources_targets = sources_targets.dropna()
    return sources_targets


def get_sources_targets():
    visits = []
    frames = []
    most_visited = {}

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            frames.append(get_sources_targets_for(file, visits, most_visited))

    return frames, visits, most_visited


def group_renderers(renderers):
    renderer_groups = {}
    for renderer in figure_.renderers:
        if '>' in renderer.name:
            source, target = renderer.name.split('>')
            try:
                renderer_groups[source].append(renderer)
            except KeyError as e:
                renderer_groups[source] = [renderer]
        else:
            try:
                renderer_groups[renderer.name].append(renderer)
            except KeyError as e:
                renderer_groups[renderer.name] = [renderer]
    return renderer_groups


def draw_nodes(
    figure_,
    graph_data_frame,
    common_websites_frequency,
    usefull_websites,
):
    for website in graph_data_frame:
        if website in usefull_websites:
            figure_.circle_dot(
                x=graph_data_frame[website][0],
                y=graph_data_frame[website][1],
                name=website,
                size=5*common_websites_frequency[website],
                fill_color=get_random_color(),
            )
        else:
            figure_.circle(
                x=graph_data_frame[website][0],
                y=graph_data_frame[website][1],
                name=website,
                size=5*common_websites_frequency[website],
                line_width=0,
                fill_color=get_random_color(),
            )
    return True


def draw_edges(figure_, graph_data_frame, edges, number_visits):
    for source_name, target_name in edges:
        source = graph_data_frame[source_name]
        target = graph_data_frame[target_name]
        figure_.line(
            [source[0], target[0]],
            [source[1], target[1]],
            line_color='black',
            line_width=number_visits[
                f'{source_name}>{target_name}'
            ]/max(number_visits.values())*5,
            name=f'{source_name}>{target_name}',
        )
    return True


def get_network(sources_targets, most_common_websites):
    graph_nx = nx.DiGraph()
    for source in sources_targets['source'].drop_duplicates():
        if source in most_common_websites:
            graph_nx.add_node(source)
    for edge in sources_targets.itertuples():
        if edge.source in most_common_websites and edge.target in most_common_websites:
            graph_nx.add_edge(
                edge.source,
                edge.target,
            )
    return graph_nx


def get_most_common_website_participents(most_visited):
    common_websites = []

    for key in most_visited.keys():
        most_visited[key] = Counter(most_visited[key])
        common_websites += most_visited[key].keys()

    common_websites_frequencies = Counter(common_websites)

    cut_off = int(
        input(
            'The cutoff value for the number of participent: '
        )
    )
    most_common_websites = [
        website for website, frequency in common_websites_frequencies.items()
        if frequency >= cut_off
    ]
    return most_common_websites, common_websites_frequencies


if __name__ == "__main__":
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    post_survey = pd.read_csv('data/post_survey.csv')
    usefull_websites = set(get_usefull_websites(post_survey))
    os.chdir(os.getcwd() + os.sep + 'Persona')

    frames, visits, most_visited = get_sources_targets()

    (
        most_common_websites,
        common_websites_frequencies
    ) = get_most_common_website_participents(most_visited)

    sources_targets = pd.concat(frames)
    number_visits = Counter(visits)
    graph_nx = get_network(sources_targets, most_common_websites)
    graph_data_frame = pd.DataFrame(nx.spring_layout(graph_nx, scale=2))

    figure_ = figure(
        title=f"Graph Usefullwebpages",
        x_range=(-2.1,2.1),
        y_range=(-2.1,2.1),
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
    figure_.outline_line_width = 0

    draw_edges(
        figure_,
        graph_data_frame,
        graph_nx.edges,
        number_visits,
    )
    draw_nodes(
        figure_,
        graph_data_frame,
        common_websites_frequencies,
        usefull_websites,
    )

    renderer_groups = group_renderers(figure_.renderers)

    legend = Legend(
        items=[
            LegendItem(
                label=f'{key}',
                renderers=value,
            )
            for key, value in renderer_groups.items()
        ]
    )
    figure_.add_layout(legend, 'right')
    figure_.legend.click_policy = 'hide'
    figure_.legend.location = 'right'
    figure_.legend.orientation = 'vertical'
    figure_.legend.background_fill_alpha=.6
    figure_.output_backend = 'svg'
    show(figure_)
