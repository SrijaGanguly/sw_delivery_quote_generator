# This script contains several utility methods that the project depends on
import requests
import pandas as pd

def get_resource_data(url):
    """
    common helper to fetch properties list from swapi.tech response of individual object
    :param url: Almost always a string represnting the hostname
    :return: List of "properties" within the "request" block in the response Or None
    """
    try:
        api_url = url
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()["result"]
        properties = [element['properties'] for element in data]
        return properties
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