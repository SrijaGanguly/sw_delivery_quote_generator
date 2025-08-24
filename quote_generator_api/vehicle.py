import pandas as pd
from quote_generator_api import globals

from quote_generator_api.utility import get_resource_data, convert_to_df, concat_df

def pull_vehicle_data(vehicle_name):
    """
    Pull vehicle data from given a vehicle name
    :param vehicle_name: name of the vehicle to fetch data for
    :return: list of vehicle properties or None
    """
    if vehicle_name not in [None, ""]:
        return get_resource_data(f"${globals.BASE_URL}/vehicles?name=${vehicle_name}")
    return None

#todo method may change based on api hostname difference
def create_vehicle_df(vehicle_name_list):
    """
    Create a dataframe of vehicle data by gathering individual vehicle data from the input list.
    :param vehicle_name_list: list of vehicle names to make data
    :return: dataframe with vehicle names, url and uid Or None
    """
    df = pd.DataFrame()
    for vehicle in vehicle_name_list:
        vehicle_data = pull_vehicle_data(vehicle)
        if vehicle_data is not None:
            df = concat_df(df, convert_to_df(vehicle_data))
    return df