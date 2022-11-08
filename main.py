import os
import pandas as pd
import matplotlib.pyplot as plt
from urllib.parse import urlparse


def calculate_time_spends(data_frame):
    time_spend = []
    actual_time = pd.to_datetime(data_frame['DateUTC'][0])

    for i in range(len(data_frame)):
        time_spend.append((pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds()) 
        # if (pd.to_datetime(data_frame['DateUTC'][i]) - actual_time).total_seconds() > 300:
        #     print(data_frame['Tab_URL'][i])
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
    # fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

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
            data_frame = data_frame.groupby('Web_site', as_index = False).sum()
            print(data_frame['Web_site'])
            ax = data_frame.plot(kind = 'barh', x = 'Web_site', y = 'time_spend', legend = False, title=file.split('.')[0])
            ax.set_xlabel('Time spend')
            ax.set_ylabel('')
            plt.tight_layout()
            #plt.savefig(f'{file.split(".")[0]}.svg')
            #plt.show()
            # ax.hist(data_frame['Web_site'], data_frame['time_spend'], label=file.split('.')[0])  # Plot some data on the axes.
            # ax.set_xlabel('Time point')  # Add an x-label to the axes.
            # ax.set_ylabel('Time Duration')  # Add a y-label to the axes.
            
            

       
    # ax.set_title("Simple Plot")  # Add a title to the axes.
    # ax.legend()  # Add a legend.
    # plt.show()

    



