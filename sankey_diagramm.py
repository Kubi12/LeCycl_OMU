from matplotlib.sankey import Sankey
import os
import pandas as pd 
from urllib.parse import urlparse


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

# new dataframe with usactions: 
# use maybe: pandas.core.groupby.DataFrameGroupBy.agg 



# – User action: The type of the user action. It can be one of the following:
# TabCreate, TabActivate, TabUpdate, TabRemove, ClipboardCopy, and WindowScroll. 
# Start: Tabcreate
# second: Tabactivate, Tabupdate 
# clipbord copy for new search? 
# tabremove : finish
# https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0