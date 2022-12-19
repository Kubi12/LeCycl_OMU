import os
import pandas as pd
import json

from utils import get_network_location, clean_website


def get_all_websites():
    current_directory = os.getcwd()
    os.chdir(os.path.join(current_directory, 'Persona'))
    websites = set()
    for file in os.listdir():
        if 'csv' in file:
            data_frame = pd.read_csv(file)
            data_frame['Web_site'] = data_frame['Tab_URL'].apply(
                get_network_location,
            )
            data_frame['Web_site'] = data_frame['Web_site'].apply(
                clean_website,
            )
            websites = websites | set(data_frame['Web_site'])
    os.chdir(current_directory)
    return websites


def titelize(category):
    return ' '.join(category.split('_')).title()


def get_categories():
    current_directory = os.getcwd()
    os.chdir(os.path.join(current_directory, 'Categorization'))
    categories = {}
    for file in os.listdir():
        if 'json' in file:
            category = titelize(file.split('.')[0][:-1])
            with open(file, 'r') as json_file:
                websites = json.load(json_file)
            categories[category] = websites
    os.chdir(current_directory)
    return categories


def assign_category():
    websites = get_all_websites()
    categories = get_categories()
    websites_categories = {}
    for website in websites:
        if website:
            for category, websites_ in categories.items():
                if website in websites_:
                    websites_categories[website] = category
    return websites_categories


if __name__ == '__main__':
    current_directory = os.getcwd()
    os.chdir(os.path.join(current_directory, 'Categorization'))
     
     # For the control, that webpages are not commen 2 times.
    websites_categorized = set()
    json_files_done = [
        'Q&A_websites.json',
        #'not_task_relateds.json',
        'search_engines.json',
        'technical_blogs.json',
        'linguistics_websites.json',
        'official_references.json',
        'social_medias.json',
        'video_references.json',
    ]
    for file in json_files_done:
        with open(file, 'r') as json_file:
            try:
                websites = set(json.loads(json_file.read()))
            except Exception as e:
                print(e, file)
        websites_categorized = websites_categorized | websites
    for file in os.listdir():
        if 'json' in file and file not in json_files_done:
            with open(file, 'r') as json_file:
                try:
                    websites = set(json.load(json_file))
                except Exception as e:
                    print(file)
            websites = websites - websites_categorized
            with open(file, 'w') as json_file:
                json.dump(list(websites), json_file, indent=4)
    os.chdir(current_directory)