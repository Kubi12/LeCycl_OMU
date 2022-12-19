import os
import pandas as pd
from urllib.parse import urlparse
from network_diagramm import get_network_location


def get_artikel(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.path
    

if __name__ == "__main__":
    os.chdir(os.getcwd() + os.sep + 'Persona')

    for file in os.listdir():
        if len(file.split('.')) == 2 and file.split('.')[1] == 'csv':
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(get_artikel)
            data_frame = data_frame.loc['towardsdatascience.com' in data_frame.Tab_URL]
            print(data_frame)