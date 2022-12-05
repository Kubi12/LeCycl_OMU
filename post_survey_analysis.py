from collections import Counter
import pandas as pd
from urllib.parse import urlparse
import holoviews as hv
from holoviews import opts, dim
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


if __name__ == '__main__':
    post_survey = pd.read_csv('data/post_survey.csv')
    create_visualisation(get_usefull_websites_frequencies(post_survey))
