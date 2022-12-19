from collections import Counter
import networkx as nx
from random import randrange
import os
import pandas as pd
from urllib.parse import urlparse
from bokeh.plotting import show, figure
from bokeh.models import Legend, LegendItem

from utils import clean_website, get_category
from assign_category import assign_category


TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,hover"


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append(
            (
                pd.to_datetime(data_frame['DateUTC'][i]) - actual_time
            ).total_seconds() / 60
        )
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc


def add_category_most_visited(file, most_visited, current_category, next_category):
    try:
        if current_category:
            most_visited[
                f'{file.split(".")[0]}'
            ].append(current_category)
    except KeyError:
        if current_category:
            most_visited[
                f'{file.split(".")[0]}'] = [current_category]
    try:
        if next_category:
            most_visited[
                f'{file.split(".")[0]}'].append(next_category)
    except KeyError:
        if next_category:
            most_visited[
                f'{file.split(".")[0]}'] = [next_category]


def get_sources_targets_for(file, visits, most_visited, websites_categories):
    data_frame = pd.read_csv(file)
    data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
    data_frame['Web_site'] = data_frame['Web_site'].apply(clean_website)
    data_frame['category'] = data_frame['Web_site'].apply(
        lambda x: get_category(websites_categories, x)
    )
    time_spend = calculate_time_spends(data_frame)
    data_frame['time_spend'] = pd.Series(time_spend)
    sources_targets = []
    for index, item in enumerate(data_frame.itertuples()):
        if index == 0:
            continue
        current_category, next_category = (
            data_frame['category'][index-1],
            item.category,
        )
        add_category_most_visited(
            file,
            most_visited,
            current_category,
            next_category,
        )
        if current_category == next_category:
            if sources_targets:
                sources_targets[-1][-1] += float(
                    data_frame['time_spend'][index]
                )
                continue
        if current_category and next_category:
            visits.append(f'{current_category}>{next_category}')
            sources_targets.append([
                data_frame['category'][index-1],
                item.category,
                data_frame['time_spend'][index-1],
            ])
    sources_targets = pd.DataFrame(sources_targets)
    sources_targets = sources_targets.rename(
        columns={0: 'source', 1: 'target', 2: 'value',},
    )
    sources_targets = sources_targets.dropna()
    return sources_targets


def get_sources_targets(websites_categories):
    frames = []
    visits = []
    most_visited = {}
    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            frames.append(
                get_sources_targets_for(
                    file,
                    visits,
                    most_visited,
                    websites_categories,
                )
            )
    return frames, visits, most_visited


def get_random_hex():
    return hex(randrange(17, 255))[2:].upper()


def get_random_color():
    return f'#{get_random_hex()}{get_random_hex()}{get_random_hex()}'


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
    common_categories_frequency,
):
    for category in graph_data_frame:
        figure_.circle(
            x=graph_data_frame[category][0],
            y=graph_data_frame[category][1],
            name=category,
            size=5*common_categories_frequency[category],
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


def get_network(sources_targets):
    graph_nx = nx.DiGraph()
    graph_nx.add_nodes_from(sources_targets['source'].drop_duplicates())
    for edge in sources_targets.itertuples():
        graph_nx.add_edge(
            edge.source,
            edge.target,
        )
    return graph_nx


if __name__ == "__main__":
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    websites_categories = assign_category()
    os.chdir(os.getcwd() + os.sep + 'Persona')

    frames, visits, most_visited = get_sources_targets(websites_categories)
    sources_targets = pd.concat(frames)
    common_categories = []

    for key in most_visited.keys():
        most_visited[key] = Counter(most_visited[key])
        common_categories += most_visited[key].keys()

    common_categories_frequencies = Counter(common_categories)
    number_visits = Counter(visits)
    graph_nx = get_network(sources_targets)
    graph_data_frame = pd.DataFrame(nx.spring_layout(graph_nx, scale=2))

    figure_ = figure(
        title=f"Graph TOBEFILLED",
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
        common_categories_frequencies,
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