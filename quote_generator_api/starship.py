from quote_generator_api.globals import BASE_URL
from quote_generator_api.utility import get_overview_json, get_resource_data, convert_to_df


#todo function may change with change in source host
def pull_starships_urls():
    """
    method to bring all starship urls available in the api
    :return: list data of url
    """
    overview_data = get_overview_json(BASE_URL+"/starships?page=1&limit=40")
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

def find_min_crew(crew):
    """
    function to find the minimum crew travelling distance
    :param crew: the number of crew as mentioned in the starship properties in different formats
    :return: minimum crew from the crew mentioned
    """

    if crew.isdigit():
        return crew
    elif "," in crew:
        return crew.replace(',', '')
    elif "-" in crew:
        return crew.split("-")[0]
    else:
        return "-1"


def calculate_num_days_travel(starship_mglt, distance_mglt):
    """
    function to calculate the number of days travel using the distance in MegaLights as input
    :param distance_mglt: distance in MegaLights as input
    :param starship_mglt: mglt property associated to starship as max speed
    :return: number of days to travel in string in Earth hours where 24 hours is 1 day
    """
    if starship_mglt.isnumeric() and float(starship_mglt) > 0:
        days_travel = (float(distance_mglt) / float(starship_mglt))*2
        return str(days_travel / 24)
    else:
        return "NA"

def calculate_crew_cost(min_crew, num_days_travel):
    """
    function to calculate the crew cost for min crew travelling the distance
    :param min_crew: minimum crew travelling distance
    :param num_days_travel: number of days travelling distance
    :return: cost of delivery in string
    """
    try:
        if (num_days_travel.isnumeric() or float(num_days_travel)) and int(min_crew) > 0:
            return str(int(min_crew) * 100 * float(num_days_travel))
        else:
            return "NA"
    except ValueError:
        return "NA"

def calculate_starship_delivery_cost_df(starship_df, distance_mglt):
    """
    method to modify starship dataframe by adding crew cost and days of travel depending on the distance in MegaLights as input
    :param starship_df: starship dataframe with original properites as brought from the api location
    :param distance_mglt: the distance in MegaLights provided to the application
    :return: a modified dataframe with starship data
    """
    select_columns = ["name", "model", "min_crew", "MGLT", "num_days_to_travel", "cost_of_credits_delivery"]

    starship_df["min_crew"] = starship_df["crew"].apply(find_min_crew)
    starship_df["num_days_to_travel"] = starship_df["MGLT"].apply(calculate_num_days_travel, distance_mglt=distance_mglt)
    starship_df["cost_of_credits_delivery"] = starship_df.apply(lambda row: calculate_crew_cost(row["min_crew"], row["num_days_to_travel"]), axis=1)

    starship_df = starship_df[select_columns]
    return starship_df