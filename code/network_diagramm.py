from assign_category import assign_category
from utils import (
    clean_website,
    get_network_location,
    calculate_time_spends,
    get_network,
)
import networkx as nx
from datetime import timedelta
import os
import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.models import HoverTool
hv.extension('bokeh')


def get_sources_targets(data_frame):
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
    return sources_targets


def add_websites_timespend(data_frame, cutoff_time_spend=0):
    data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
    time_spend = calculate_time_spends(data_frame)
    data_frame['time_spend'] = pd.Series(time_spend)
    data_frame['time_spend'] = data_frame['time_spend'].apply(
        lambda x: min(x, cutoff_time_spend * 60)
    )
    data_frame = data_frame.reset_index()
    return data_frame


def create_sankey(file, time_spend):
    sankey = hv.Sankey(time_spend[['Start', 'Web_site', 'Percentage']])
    sankey.opts(
        title=f'Sankey-{file.split(".")[0]}',
        label_position='left',
        edge_color='Start',
        node_color='index',
    )
    renderer = hv.renderer('bokeh')
    renderer.save(sankey, f'sankey-{file.split(".")[0]}')
    return sankey


def create_chord(file, sources_targets):
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
    renderer.save(chord, f'chord-{file.split(".")[0]}')
    return chord


def get_time_spend(data_frame):
    time_spend = data_frame[['Web_site', 'time_spend']].dropna()
    time_spend = time_spend.groupby(['Web_site'], as_index=False).sum()
    total_time = sum(time_spend['time_spend'])
    time_spend = pd.DataFrame(time_spend)
    time_spend['Percentage'] = time_spend['time_spend'] / total_time * 100
    time_spend['Start'] = f'Total time: {timedelta(seconds=int(total_time))}'
    return time_spend


def get_frame(file, cutoff_time_spend=0, with_sources_targets=True):
    data_frame = add_websites_timespend(
        pd.read_csv(file),
        cutoff_time_spend=cutoff_time_spend,
    )
    time_spend = get_time_spend(data_frame)
    patricipent = ' '.join(file.split(".")[0].split('_'))
    time_spend['Participent'] = f'{patricipent}'
    if with_sources_targets:
        sources_targets = get_sources_targets(data_frame)
        return time_spend, sources_targets
    else:
        return time_spend


def create_visualization_data(filtered_all_frames):
    visualization_data = pd.DataFrame()
    visualization_data['Start'] = pd.concat(
        [filtered_all_frames['Start'],
         filtered_all_frames['Web_site']],
        ignore_index=True,
    )
    visualization_data['End'] = pd.concat(
        [filtered_all_frames['Web_site'],
         filtered_all_frames['Participent']],
        ignore_index=True,
    )
    visualization_data['Web_site'] = pd.concat(
        [filtered_all_frames['Web_site'],
         filtered_all_frames['Web_site']],
        ignore_index=True,
    )
    visualization_data['Percentage'] = pd.concat(
        [filtered_all_frames['Percentage'],
         filtered_all_frames['Percentage']],
        ignore_index=True,
    )
    visualization_data['timedelta'] = pd.concat(
        [filtered_all_frames['timedelta'],
         filtered_all_frames['timedelta']],
        ignore_index=True,
    )
    return visualization_data


def prepare_data(data):
    total_time = int(sum(data['time_spend']))
    data['Percentage'] = data['time_spend'] / total_time * 100
    data['timedelta'] = data['time_spend'].apply(
        lambda x: str(timedelta(seconds=int(x))),
    )
    data['Web_site'] = data['Web_site'].apply(clean_website)
    data['Start'] = f'Total time: {timedelta(seconds=int(total_time))}'
    return data


def get_sankey_participents(visualization_data):
    sankey = hv.Sankey(
        visualization_data[
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
    sankey.opts(
        title=f'TOBEFILLED',
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
    return sankey


def create_sankey_participents(frames):
    all_frames = prepare_data(pd.concat(frames))
    total_time = sum(all_frames['time_spend'])
    cut_off = float(input('The cut-off duration to each website in min: '))
    cut_off = (cut_off * 60) / total_time * 100
    filtered_all_frames = all_frames[all_frames.Percentage > cut_off]
    visualization_data = create_visualization_data(filtered_all_frames)
    print('Total percentage:', sum(filtered_all_frames['Percentage']))
    renderer = hv.renderer('bokeh')
    sankey = get_sankey_participents(visualization_data)
    renderer.save(sankey, f'sankey-all')
    return True


if __name__ == "__main__":
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    websites_categories = assign_category()
    os.chdir(os.getcwd() + os.sep + 'Persona')
    frames = []
    cutoff_time_spend = int(
        input('Max time spend in one session in minutes: ')
    )

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            (
                time_spend,
                sources_targets,
            ) = get_frame(file, cutoff_time_spend=cutoff_time_spend)
            create_chord(file, sources_targets)
            create_sankey(file, time_spend)
            frames.append(time_spend)

    create_sankey_participents(frames)
