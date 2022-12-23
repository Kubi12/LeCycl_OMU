import pandas as pd
from urllib.parse import urlparse
from random import randrange


def get_category(websites_categories, website):
    return websites_categories.get(website)


def clean_website(website):
    if website:
        if 'www' in website:
            return '.'.join(website.split('.')[1:])
        return website


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append(
            (
                pd.to_datetime(data_frame['DateUTC'][i]) - actual_time
            ).total_seconds()
        )
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network(sources_targets):
    graph_nx = nx.DiGraph()
    for source in sources_targets['source'].drop_duplicates():
        graph_nx.add_node(source)
    for edge in sources_targets.itertuples():
        graph_nx.add_edge(edge.source, edge.target)
    return graph_nx


def get_random_hex():
    return hex(randrange(17, 255))[2:].upper()


def get_random_color():
    return f'#{get_random_hex()}{get_random_hex()}{get_random_hex()}'
