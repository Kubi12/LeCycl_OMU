from datetime import timedelta
import networkx as nx
import math
import os
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import holoviews as hv
import plotly.graph_objects as go

from assign_category import assign_category
from utils import clean_website, calculate_time_spends, get_network_location
from all_network_diagramm_categorized import get_sources_targets_for


if __name__ == "__main__":
    websites_categories = assign_category()
    # os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    os.chdir(os.getcwd() + os.sep + 'Persona')
    website_color = {}

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            data_frame['Web_site'] = data_frame['Web_site'].apply(clean_website)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            sources_targets = get_sources_targets_for(file, [], {}, websites_categories)
            categories = []
            categories = list(
                set(sources_targets['source']) | set(sources_targets['target'])
            )
            sources, targets, values = [], [], []
            for index, tuple_ in enumerate(sources_targets.itertuples()):
                sources.append(categories.index(tuple_.source))
                targets.append(categories.index(tuple_.target))
                values.append(tuple_.value)
            num_categories = list(set(categories))
            fig = go.Figure(go.Sankey(
                name=f'{file.split(".")[0]}-Sankey',
                arrangement = "fixed",
                node = {
                    "label": categories,
                    "x": np.linspace(1/8, 7/8, num=len(num_categories)),
                    'y': np.linspace(1/8, 7/8, num=len(num_categories)),
                    'pad': 10,
                },
                link = {
                    "source": sources,
                    "target": targets,
                    "value": values,
                },
            ))
            participent = ' '.join(file.split('.')[0].split('_'))
            total_time_spend = timedelta(
                minutes=sum(sources_targets["value"])
            )
            fig.update_layout(
                title={
                    'text': f'{participent}, SumTimeSpend: {total_time_spend}'
                },
                showlegend=True,
                legend={
                    'title': 'Categories',
                    'font': {
                        'size': 10,
                    },
                    'bgcolor': 'black',
                },
            )
            fig.show(
                config=dict(
                    {'scrollZoom': True,'displayModeBar': True}
                )
            )
