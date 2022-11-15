import os
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import grid
from bokeh.transform import cumsum
import random
from math import pi

def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() / 60) 
        # if (pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() > 300:
        #     print(data_frame['Tab_URL'][i])
        actual_time = pd.to_datetime(data_frame['DateUTC'][i])

    return time_spend

# all except https or http as none
def get_network_location(url): 
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc

def get_color(website_color, website):
    if website in website_color.keys():
        return website_color[website]
    else: 
        color = f"#{hex(random.randint(50, 255))[2:]}{hex(random.randint(20, 255))[2:]}{hex(random.randint(20, 255))[2:]}"
        website_color[website] = color
        return color

#Automated reading of the files. Makes life easier: os
def plot_timespend_webpages():
    os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend) 
            # ax.plot(list(range(len(data_frame))), time_spend, label=file.split('.')[0])  # Plot some data on the axes.
            # ax.set_xlabel('Time point')  # Add an x-label to the axes.
            # ax.set_ylabel('Time Duration')  # Add a y-label to the axes.
            
            # print("max: " , max(time_spend))
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            data_frame_sum_time_spend = data_frame.groupby('Web_site', as_index = False).sum()
            data_frame_sum_time_spend_avg = data_frame.groupby('Web_site', as_index = False).mean()
            data_frame_avg_scroll_speed = data_frame.groupby('Web_site', as_index = False).mean()
            fig, ax = plt.subplots(nrows = 2,  layout='constrained')
            data_frame_sum_time_spend.plot(ax = ax[0], kind = 'barh', x = 'Web_site', y = 'time_spend',label= "Time spend(sum)", legend = True, title=file.split('.')[0])
            data_frame_sum_time_spend_avg.plot(ax = ax[0],color= "red", kind = 'barh', x = 'Web_site', y = 'time_spend', label= "Time spend(avg)", legend = True, title=file.split('.')[0])
            data_frame_avg_scroll_speed.plot(ax = ax[1], color = "green", kind ='barh', x = 'Web_site', y = 'Scroll_YAxisSpeed', legend = False, title=file.split('.')[0] )
            #ax.set_xlabel('Time spend')
            ax[0].set_ylabel('')
            ax[1].set_ylabel('')
            ax[0].set_xlabel('Time spend(min)')
            ax[1].set_xlabel('Scroll speed')


#Automated reading of the files. Makes life easier: os
if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'Datenanalyse/Persona')
    random.seed(1)
    frames = []
    figures = []
    website_color = {}

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            time_spend = calculate_time_spends(data_frame)
            data_frame['time_spend'] = pd.Series(time_spend)
            #data_frame['color'] = data_frame.apply(lambda x : get_color())
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_network_location)
            data_frame_sum_time_spend = data_frame.groupby('Web_site', as_index = False).sum()
            data_frame_sum_time_spend = pd.DataFrame(data_frame_sum_time_spend)
            data_frame_sum_time_spend['color'] = data_frame_sum_time_spend['Web_site'].apply(lambda website : get_color(website_color, website))
            data_frame_sum_time_spend['angle'] = data_frame_sum_time_spend['time_spend']/data_frame_sum_time_spend['time_spend'].sum() * 2*pi
            #print(data_frame_sum_time_spend.head)
            frames.append(data_frame)
            figure_ = figure(title = file.split('.')[0])
            figures.append(figure_)

            pie = figure_.wedge(
                x=0, 
                y=1, 
                radius=0.6, 
                start_angle=cumsum('angle', include_zero=True), 
                end_angle=cumsum('angle'),
                line_color= None, 
                fill_color='color',
                fill_alpha = 0.9, 
                legend_field='Web_site', 
                source= data_frame_sum_time_spend)

            figure_.axis.axis_label = None
            figure_.axis.visible = False
            figure_.grid.grid_line_color = None
            figure_.legend.background_fill_alpha = 0.5
        
    
    grid = grid(figures, nrows= 3)
    show(grid)
 
