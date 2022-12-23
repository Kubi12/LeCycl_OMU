import networkx as nx
from datetime import timedelta
import os
import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.models import HoverTool
hv.extension('bokeh')


from utils import (
    clean_website,
    get_network_location,
    calculate_time_spends,
    get_network,
    get_category
)
from assign_category import assign_category
from network_diagramm import (
    get_frame,
    get_sources_targets,
    add_websites_timespend,
    get_time_spend,
)


def create_visualization_data(filtered_all_frames):
    visualization_data = pd.DataFrame()
    visualization_data['Start'] = pd.concat(
        [filtered_all_frames['Start'],
        filtered_all_frames['category']],
        ignore_index=True,
    )
    visualization_data['End'] = pd.concat(
        [filtered_all_frames['category'],
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
    data['category'] = data['Web_site'].apply(
        lambda x: get_category(websites_categories, x)
    )
    data['Start'] = f'Total time: {timedelta(seconds=int(total_time))}'
    return data


def get_sankey_participents_categorized(visualization_data):
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


def create_sankey_participents_categorized(frames):
    all_frames = prepare_data(pd.concat(frames))
    total_time = sum(all_frames['time_spend'])
    cut_off = float(input('The cut-off duration to each website in min: '))
    cut_off = (cut_off * 60) / total_time * 100
    filtered_all_frames = all_frames[all_frames.Percentage > cut_off]
    visualization_data = create_visualization_data(filtered_all_frames)
    print('Total percentage:', sum(filtered_all_frames['Percentage']))
    renderer = hv.renderer('bokeh')
    sankey = get_sankey_participents_categorized(visualization_data)
    renderer.save(sankey, f'sankey-all-categorized')
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
            frames.append(
                get_frame(
                    file,
                    cutoff_time_spend=cutoff_time_spend,
                    with_sources_targets=False,
                )
            )

    create_sankey_participents_categorized(frames)
