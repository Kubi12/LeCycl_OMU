import networkx as nx
import math
import os
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import holoviews as hv
import plotly.graph_objects as go

from all_network_diagramm import get_sources_targets_for
from utils import calculate_time_spends, get_network_location


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
            sources_targets = get_sources_targets_for(file, [], {})
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
            total_time_spend = sum(sources_targets["value"])
            fig.update_layout(
                title={
                    'text': f'{participent}, SumTimeSpend: {total_time_spend:.2f} min'},
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
