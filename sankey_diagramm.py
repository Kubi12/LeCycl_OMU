# from matplotlib.sankey import Sankey
import networkx as nx
import math
import os
import pandas as pd
from urllib.parse import urlparse
import holoviews as hv
from holoviews import opts, dim
# from bokeh.plotting import show, figure, from_networkx
# from bokeh.models import Ellipse, GraphRenderer, StaticLayoutProvider, Legend
# from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
#                                                     MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
# from bokeh.palettes import Spectral8, inferno, viridis, Spectral4
hv.extension('bokeh')

def reduce_(item, next):
    pass

def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() / 60)
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend

def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc

if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    frames = []
    figures = []
    website_color = {}


    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            renderer = hv.renderer('bokeh')
            data_frame = data_frame[['Web_site', 'time_spend']].dropna()
            data_frame = data_frame.reindex(range(len(data_frame)))
            sources_targets = []
            sites_visited = {}

            for index, item in enumerate(data_frame.itertuples()):
                #print(sources_targets)
                if index + 1 == len(data_frame):
                    break
                current_website, next_website = (
                    item.Web_site,
                    data_frame['Web_site'][index+1],
                )
                if current_website == next_website:
                    if sources_targets:
                        sources_targets[-1][-1] += float(
                            data_frame['time_spend'][index]
                        ) * 60
                        continue
                try:
                    visite = sites_visited[current_website]
                    sites_visited[current_website] += 1
                except KeyError:
                    sites_visited[current_website] = 1
                try:
                    sources_targets.append([
                        f'{current_website}-{sites_visited[current_website]}',
                        f'{next_website}-{sites_visited[next_website]}',
                        item.time_spend * 60,
                    ])
                    sites_visited[next_website] += 1
                except KeyError:
                    sources_targets.append([
                        f'{current_website}-{sites_visited[current_website]}',
                        f'{next_website}-{1}',
                        item.time_spend * 60,
                    ])
                    sites_visited[next_website] = 1

            sources_targets = pd.DataFrame(sources_targets)
            sources_targets = sources_targets.rename(
                columns={0: 'source', 1: 'target', 2: 'value',},
            )
            print(sources_targets)
            sankey = hv.Sankey(sources_targets)
            sankey.opts(
                label_position='left',
                edge_color='target',
                node_color='index',
            )
            sankey.opts(width=2000, height=1000)
            renderer.save(sankey, 'sankey.html')
            break
