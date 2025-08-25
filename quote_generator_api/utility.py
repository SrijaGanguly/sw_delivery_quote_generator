# This script contains several utility methods that the project depends on
import requests
import json
import pandas as pd

def get_resource_data(url):
    """
    common helper to fetch properties list from swapi.tech response of individual object
    :param url: Almost always a string represnting the hostname and the api location
    :return: List of "properties" within the "result" block in the response Or None
    """
    try:
        api_url = url
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()["result"]
        if isinstance(data, dict):
            return [data["properties"]]
        elif isinstance(data, list):
            return [item["properties"] for item in data if "properties" in item]
    except requests.exceptions.RequestException as err:
        print(err)
        return None

def get_overview_json(url):
    """
    common helper to fetch overview data from swapi.tech for a resource
    :param url: string representing the hostname and the api location
    :return: list of json data of "results" block in the response Or None
    """
    try:
        api_url = url
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()["results"]
    except requests.exceptions.RequestException as err:
        print(err)
        return None

def convert_to_df(data):
    """
    converts any data to pandas dataframe
    :param data: the data to convert
    :return: dataframe representation of the data
    """
    return pd.DataFrame(data)

def convert_df_to_json(df):
    """
    converts pandas dataframe to json
    :param df: dataframe to convert
    :return: json representation of the dataframe
    """
    return df.to_json(orient="records")

def concat_df(df1, df2, by_row=True):
    """
    concatenate two dataframes into one dataframe
    :param df1: first dataframe
    :param df2: second dataframe
    :param by_row: a boolean value that if True will concatenate by rows else by columns
    :return:
    """
    if by_row:
        return pd.concat([df1, df2], axis=0, ignore_index=True)
    else:
        return pd.concat([df1, df2], axis=1)

def filter_df(df, column_name, value, remove_values=False):
    """
    Filters dataframe rows based on a certain column name and value(s) provided
    :param df: dataframe to filter
    :param column_name: the column name to filter the dataframe on
    :param value: the value to filter the dataframe on
    :param remove_values: boolean value when True will remove the rows that have the column value. By default it is False to remove the rows not with the column value.
    :return: filtered new dataframe
    """
    if remove_values:
        return df[~df[column_name].isin([value])]
    else:
        return df[df[column_name].isin([value])]

def convert_col_to_numeric(df, orig_col, new_col):
    df = df.copy()
    df.loc[:, new_col] = pd.to_numeric(df[orig_col], errors="coerce")
    return df

def sort_df_by_numeric_col(df, sort_by, ascending=True):
    """
    function to sort dataframe by temporary numeric column while resetting index and then the numeric column is dropped
    :param df: dataframe to sort with the data
    :param sort_by: column name to sort by
    :param ascending: sort in ascending or descending
    :return:
    """
    df = (df
          .sort_values(by=sort_by, ascending=ascending)
          .reset_index(drop=True)
          .drop(columns=sort_by))
    return df

def write_multiple_df_to_json(df_list: list[pd.DataFrame], key_list: list[str], file_path=""):
    """
    function to write multiple dataframes to json with key values for each block of data
    :param df_list: the list of dataframes to write
    :param key_list: the list of key values to write for each of the dataframe block
    :param file_path: the path of the file to write to in json
    :return: writes to a json file and returns nothing
    """
    if len(df_list) != len(key_list):
        print("Length of df_list and key_list are not equal")
        return
    concat_df_with_key = {key: df.to_dict(orient="records") for key, df in zip(key_list, df_list)}
    with open(file_path+"sales_vehicle_delivery_quote.json", "w") as output_file:
        json.dump(concat_df_with_key, output_file, indent=4)