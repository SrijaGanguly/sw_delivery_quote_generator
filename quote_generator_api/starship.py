from quote_generator_api import globals
from quote_generator_api.utility import get_overview_json, get_resource_data, convert_to_df


#todo function may change with change in source host
def pull_starships_urls():
    """
    method to bring all starship urls available in the api
    :return: list data of url
    """
    overview_data = get_overview_json(f"${globals.BASE_URL}/starships?page=1&limit=40")
    if overview_data is not None and len(overview_data) > 0:
        return [res['url'] for res in overview_data]
    return None

def pull_starship_data_using_urls():
    """
    function to pull starships data using the list of urls representing the resources
    :return: list of starship properties or empty list
    """
    url_list = pull_starships_urls()
    starship_data = []
    if url_list is not None:
        for url in url_list:
            starship_property = get_resource_data(url)
            if starship_property is not None:
                starship_data = starship_data + starship_property
    return starship_data

def create_starship_df():
    """
    function to create a Dataframe of all starship details with the starship list of properties
    :return: dataframe of all starship data
    """
    return convert_to_df(pull_starship_data_using_urls())