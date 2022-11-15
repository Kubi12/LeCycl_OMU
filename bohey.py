import networkx as nx

from bokeh.palettes import Category20_20
from bokeh.plotting import figure, from_networkx, show
import os
import pandas as pd
from urllib.parse import urlparse


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() / 60) 
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend

# all except https or http as none
def get_network_location(url): 
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc



#Automated reading of the files. Makes life easier: os
if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend) 
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            #data_frame_sum_time_spend = data_frame.groupby('Web_site', as_index = False).sum()
            #data_frame_sum_time_spend_avg = data_frame.groupby('Web_site', as_index = False).mean()
            #data_frame_avg_scroll_speed = data_frame.groupby('Web_site', as_index = False).mean()

df = pd.data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location) 
     
G = nx.from_pandas_edgelist(df)


p = figure(x_range=(-2, 2), y_range=(-2, 2),
           x_axis_location=None, y_axis_location=None,
           tools="hover", tooltips="index: @index")
p.grid.grid_line_color = None

graph = from_networkx(G, nx.spring_layout, scale=1.8, center=(0,0))
p.renderers.append(graph)

# Add some new columns to the node renderer data source
graph.node_renderer.data_source.data['index'] = list(range(len(G)))
graph.node_renderer.data_source.data['colors'] = Category20_20

graph.node_renderer.glyph.update(size=20, fill_color="colors")

show(p)