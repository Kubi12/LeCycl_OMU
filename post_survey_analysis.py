from collections import Counter
import pandas as pd
from urllib.parse import urlparse
import holoviews as hv
from holoviews import opts, dim
from bokeh.models import HoverTool
hv.extension('bokeh')


def get_network_location(entry):
    components = urlparse(entry)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc
    else:
        return components.path


def get_usefull_websites(post_survey):
    usefull_websites = []
    for task in range(1, 4):
        usefull_websites += list(
            post_survey[
                f'Could you tell me the best website you find  for task {task}'
                f' that supported your answer?\nIf you haven\'t use any '
                f'website type none. (Add URL here)'
            ]
        )
    usefull_websites = list(
        map(
            get_network_location,
            list(
                map(
                    lambda x: x.lower(),
                    usefull_websites,
                )
            ),
        )
    )
    return usefull_websites


def get_usefull_websites_participents(post_survey):
    usefull_websites = []
    for task in range(1, 4):
        task_ = f'''Could you tell me the best website you find  for task {task} that supported your answer?\nIf you haven\'t use any website type none. (Add URL here)'''
        data = post_survey[ [task_,'メールアドレス',] ]
        data = data.rename(
            columns={
                task_: 'website',
                'メールアドレス': 'participent',
            }
        )
        data['Task'] = f'Task {task}'
        usefull_websites.append(
            data
        )
    usefull_websites = pd.concat(usefull_websites, ignore_index=True)
    return usefull_websites


def get_usefull_websites_frequencies(post_survey):
    usefull_websites = get_usefull_websites(post_survey)
    usefull_websites_frequency = Counter(usefull_websites)
    websites = usefull_websites_frequency.keys()
    frequencies = usefull_websites_frequency.values()
    usefull_websites_frequencies = pd.DataFrame.from_dict(
        {'websites': websites, 'frequencies': frequencies}
    )
    usefull_websites_frequencies['Start'] = f'Userfull websites'
    return usefull_websites_frequencies


def get_usefull_websites_frequencies_participents(post_survey):
    usefull_websites = get_usefull_websites_participents(post_survey)
    usefull_websites['website'] = usefull_websites['website'].apply(
        lambda x: (get_network_location(x)).lower()
    )
    usefull_websites['Start'] = 'Usefull websites'
    return usefull_websites


def create_visualisation(usefull_websites_frequencies):
    sankey = hv.Sankey(
        usefull_websites_frequencies[
            [
                'Start',
                'websites',
                'frequencies',
            ]
        ]
    )
    sankey.opts(
        title=f'Sankey-all',
        label_position='left',
        edge_color='Start',
        node_color='index',
        width=1500,
        height=1000,
    )
    renderer = hv.renderer('bokeh')
    renderer.save(sankey, f'sankey-usefull_websites')
    return sankey


def create_visualisation_with_participents(usefull_websites, with_task=True):
    to_visualise = pd.DataFrame()
    if with_task:
        to_visualise['Start'] = pd.concat(
            [usefull_websites['Task'],
            usefull_websites['website']],
            ignore_index=True,
        )
    else:
        to_visualise['Start'] = pd.concat(
            [usefull_websites['Start'],
            usefull_websites['website']],
            ignore_index=True,
        )
    to_visualise['End'] = pd.concat(
        [usefull_websites['website'],
        usefull_websites['participent']],
        ignore_index=True,
    )
    to_visualise['dummy'] = 1
    sankey = hv.Sankey(
        to_visualise[
            [
                'Start',
                'End',
                'dummy',
            ]
        ]
    )
    hover_tool = HoverTool(
        tooltips=[],
    )
    sankey.opts(
        title=f'Sankey-all',
        tools=[hover_tool],
        label_position='left',
        edge_color='End',
        node_color='index',
        width=1500,
        height=1000,
    )
    renderer = hv.renderer('bokeh')
    renderer.save(sankey, f'sankey-usefull_websites')
    return sankey


if __name__ == '__main__':
    post_survey = pd.read_csv('data/post_survey.csv')
    with_task = int(input(
        'To differentiate between tasks, enter 1, else 0:- '
    ))
    create_visualisation_with_participents(
        get_usefull_websites_frequencies_participents(
            post_survey,
        ),
        with_task=with_task,
    )