import networkx as nx
import math
import os
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import holoviews as hv
import plotly.graph_objects as go


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds())
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc


if __name__ == "__main__":
    #os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    os.chdir(os.getcwd() + os.sep + 'Persona')
    website_color = {}

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
                    data_frame['time_spend'][index],
                ])
            sources_targets = pd.DataFrame(sources_targets)
            sources_targets = sources_targets.rename(
                columns={0: 'source', 1: 'target', 2: 'value',},
            )
            sources_targets = sources_targets.dropna()
            print(f'{file.split(".")[0]}')
            print(sources_targets)

            websites = []
            for source, target in zip(sources_targets['source'], sources_targets['target']):
                if source not in websites:
                    websites.append(source)
                if target not in websites:
                    websites.append(target)
            sources, targets, values = [], [], []
            for index, tuple_ in enumerate(sources_targets.itertuples()):
                sources.append(websites.index(tuple_.source))
                targets.append(websites.index(tuple_.target))
                values.append(tuple_.value)

            fig = go.Figure(go.Sankey(
                name=f'{file.split(".")[0]}-Sankey',
                arrangement = "fixed",
                node = {
                    "label": websites,
                    "x": np.linspace(0, 1, len(websites)),
                    'y': np.linspace(1/4, 3/4, len(websites)),
                    'pad': 20,
                    'thickness': 5,
                },
                link = {
                    "source": sources,
                    "target": targets,
                    "value": values,
                },
            ))
            participent = ' '.join(file.split('.')[0].split('_'))
            total_time_spend = sum(sources_targets["value"])/60
            fig.update_layout(
                title={'text': f'{participent}, SumTimeSpend: {total_time_spend:.2f} min'},
                showlegend=True,
                autosize=True,
                legend={
                    'title': 'Websites',
                    'font': {
                        'size': 10,
                    },
                    'bgcolor': 'black',
                },
            )

            fig.show()
