from urllib.parse import urlparse


def get_category(websites_categories, website):
    return websites_categories.get(website)

#that every webpage has no www
def clean_website(website):
    if website:
        if 'www' in website:
            return '.'.join(website.split('.')[1:])
        return website


def get_network_location(url):
    components = urlparse(url)
    if components.scheme == 'https' or components.scheme == 'http':
        return components.netloc