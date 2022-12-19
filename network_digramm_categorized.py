# from matplotlib.sankey import Sankey
import networkx as nx
from datetime import timedelta
import math
import os
import pandas as pd
from urllib.parse import urlparse
import holoviews as hv
from holoviews import opts, dim
from bokeh.plotting import show, figure, from_networkx
from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend, Renderer
from bokeh.models import (
    BoxSelectTool,
    Circle,
    EdgesAndLinkedNodes,
    HoverTool,
    MultiLine,
    NodesAndLinkedEdges,
    Plot,
    Range1d,
    TapTool)
from bokeh.palettes import Spectral8, inferno, viridis, Spectral4
hv.extension('bokeh')


from utils import clean_website
from advanced_sankey_diagramm_categorized import get_category
from assign_category import assign_category


def reduce_(item, next):
    pass

# draw quadratic bezier paths


def bezier(start, end, control, steps):
    return [(1-s)**2*start + 2*(1-s)*s*control + s**2*end for s in steps]


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append(
            (pd.to_datetime(
                data_frame['DateUTC'][i]) -
                actual_time).total_seconds() /
            60)
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc


if __name__ == "__main__":
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    websites_categories = assign_category()
    os.chdir(os.getcwd() + os.sep + 'Persona')
    frames = []
    website_color = {}
    chords = []
    sankeys = []
    networks = []
    cutoff_time_spend = int(
        input(
            'Max time spend in one session in minutes: '
        )
    )

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(
                get_network_location)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            data_frame['time_spend'] = data_frame['time_spend'].apply(
                lambda x: min(x, cutoff_time_spend)
            )
            data_frame = data_frame.reset_index()
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
                columns={0: 'source', 1: 'target', 2: 'value', },
            )
            sources_targets = sources_targets.dropna()
            graph_nx = nx.DiGraph()
            for source in sources_targets['source'].drop_duplicates():
                graph_nx.add_node(source)
            for edge in sources_targets.itertuples():
                graph_nx.add_edge(edge.source, edge.target)

            time_spend = data_frame[['Web_site', 'time_spend']].dropna()
            time_spend = time_spend.groupby(['Web_site'], as_index=False).sum()
            total_time = sum(time_spend['time_spend'])
            time_spend = pd.DataFrame(time_spend)
            time_spend['Percentage'] = time_spend['time_spend'] / total_time * 100
            time_spend['Start'] = f'Total time: {total_time:.2f}'
            time_spend['color'] = '#ffffff'
            patricipent = ' '.join(file.split(".")[0].split('_'))
            time_spend['Participent'] = f'{patricipent}'
            frames.append(time_spend)
            sankey = hv.Sankey(time_spend[['Start', 'Web_site', 'Percentage']])
            sankey.opts(
                title=f'Sankey-{file.split(".")[0]}',
                label_position='left',
                edge_color='Start',
                node_color='index',
            )
            colors = ['#000000'] + hv.Cycle('Category20').values
            graph = hv.Graph.from_networkx(
                graph_nx, nx.layout.random_layout).opts(
                title=f'Network-{file.split(".")[0]}',
                node_color=dim('index').str(),
                tools=['hover'],
                node_size=20, edge_line_width=1, node_line_color='gray',
                height=1000, width=1000, show_frame=False, xaxis=None,
                yaxis=None, cmap='Category20',)
            counts = sources_targets.groupby(
                ['source', 'target']).count().reset_index()
            nodes = hv.Dataset(sources_targets[['source', 'target']])
            chord = hv.Chord((counts, nodes), ['source', 'target']).opts(
                title=f'Chord-Diagram-{file.split(".")[0]}',
                tools=['hover'],
                edge_color=dim('target').str(),
                node_color='white',
                labels='target',
                height=1000,
                width=1000,
                show_frame=True,
                xaxis=None,
                yaxis=None,
                cmap='Category20',
                edge_cmap='Category20',
            )
            renderer = hv.renderer('bokeh')
            renderer.save(sankey, f'sankey-{file.split(".")[0]}')
            renderer.save(graph, f'network-{file.split(".")[0]}')
            renderer.save(chord, f'chord-{file.split(".")[0]}')
            sankeys.append(sankey)
            chords.append(chord)
            networks.append(graph)

    all_frames = pd.concat(frames)
    total_time = sum(all_frames['time_spend'])
    all_frames['Percentage'] = all_frames['time_spend'] / total_time * 100
    total_time = timedelta(seconds=int(total_time*60))
    all_frames['Start'] = f'Total time: {total_time}'
    all_frames['timedelta'] = all_frames['time_spend'].apply(
        lambda x: str(timedelta(seconds=int(x*60))),
    )
    all_frames['Web_site'] = all_frames['Web_site'].apply(clean_website)
    all_frames['category'] = all_frames['Web_site'].apply(
        lambda x: get_category(websites_categories, x)
    )
    print(all_frames.head())
    cut_off = float(input('The cut-off duration to each website in min: '))
    cut_off = (cut_off * 60) / total_time.total_seconds() * 100
    filtered_all_frames = all_frames[all_frames.Percentage > cut_off]
    print('Total percentage:', sum(filtered_all_frames['Percentage']))
    sankey = hv.Sankey(
        filtered_all_frames[
            [
                'Start',
                'category',
                'Percentage',
                'timedelta',
                'Participent',
            ]
        ]
    )
    hover_tool = HoverTool(
        tooltips=[
            ('category', '@category'),
            ('Participent', '@Participent'),
            ('Time spend', '@timedelta'),
            ('Percentage', '@Percentage%'),
        ],
    )
    sankey.opts(
        title=f'Sankey-all',
        label_position='left',
        edge_color='Start',
        node_color='index',
        tools=[hover_tool],
        width=1500,
        height=1000,
    )
    renderer = hv.renderer('bokeh')
    renderer.save(sankey, f'sankey-all')
    sankey_ = hv.Sankey(
        filtered_all_frames[
            [
                'Participent',
                'Web_site',
                'Percentage',
                'timedelta',
            ]
        ]
    )
    hover_tool = HoverTool(
        tooltips=[
            ('Website', '@Web_site'),
            ('Participent', '@Participent'),
            ('Time spend', '@timedelta'),
            ('Percentage', '@Percentage%'),
        ],
    )
    sankey_.opts(
        title=f'Sankey-all',
        label_position='left',
        edge_color='Participent',
        node_color='index',
        tools=[hover_tool],
        width=1500,
        height=1000,
    )
    renderer = hv.renderer('bokeh')
    complex_all_frames = pd.DataFrame()
    complex_all_frames['Start'] = pd.concat(
        [filtered_all_frames['Start'],
        filtered_all_frames['category']],
        ignore_index=True,
    )
    complex_all_frames['End'] = pd.concat(
        [filtered_all_frames['category'],
        filtered_all_frames['Participent']],
        ignore_index=True,
    )
    complex_all_frames['Web_site'] = pd.concat(
        [filtered_all_frames['Web_site'],
        filtered_all_frames['Web_site']],
        ignore_index=True,
    )
    complex_all_frames['Percentage'] = pd.concat(
        [filtered_all_frames['Percentage'],
        filtered_all_frames['Percentage']],
        ignore_index=True,
    )
    complex_all_frames['timedelta'] = pd.concat(
        [filtered_all_frames['timedelta'],
        filtered_all_frames['timedelta']],
        ignore_index=True,
    )
    renderer.save(sankey + sankey_, f'sankey-all-participent')
    sankey_complex = hv.Sankey(
        complex_all_frames[
            [
                'Start',
                'End',
                'Percentage',
                'timedelta',
                'Web_site',
            ]
        ]
    )
    hover_tool = HoverTool(
        tooltips=[
            ('Website', '@Web_site'),
            ('Time spend', '@timedelta'),
            ('Percentage', '@Percentage%'),
        ],
    )
    sankey_complex.opts(
        title=f'Sankey-all',
        label_position='left',
        edge_color='End',
        node_color='index',
        tools=[hover_tool],
        width=1700,
        height=1200,
        fontsize={'labels': 30, 'yticks': 18},
        fontscale=1.5,
        padding=.1,
    )
    renderer = hv.renderer('bokeh')
    renderer.save(sankey_complex, f'sankey-all-complex')