import pandas as pd
from quote_generator_api.globals import BASE_URL

from quote_generator_api.utility import get_resource_data, convert_to_df, concat_df

#todo method may change based on api hostname difference
def pull_vehicle_data(vehicle_name):
    """
    Pull vehicle data from given a vehicle name
    :param vehicle_name: name of the vehicle to fetch data for
    :return: list of vehicle properties or None
    """
    if vehicle_name not in [None, ""]:
        return get_resource_data(BASE_URL + "/vehicles?name=" + vehicle_name)
    return None

def create_vehicle_df(vehicle_name_list):
    """
    Create a dataframe of vehicle data by gathering individual vehicle data of name and length from the input list.
    :param vehicle_name_list: list of vehicle names to make data
    :return: dataframe with vehicle names, url and uid Or None
    """
    df = pd.DataFrame()
    for vehicle in vehicle_name_list:
        vehicle_data = pull_vehicle_data(vehicle)
        if vehicle_data is not None and 'name' in convert_to_df(vehicle_data).columns:
            df = concat_df(df, convert_to_df(vehicle_data))
        else:
            print("WARNING: Vehicle {} does not exist".format(vehicle))
    if len(df) > 0:
        return df[["name","length"]]
    else:
        return pd.DataFrame()