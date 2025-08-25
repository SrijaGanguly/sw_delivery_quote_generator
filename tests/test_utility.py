import pandas as pd
import json
from unittest.mock import patch, Mock

from quote_generator_api.utility import get_resource_data, convert_to_df, convert_df_to_json, concat_df, filter_df, \
    convert_col_to_numeric, write_multiple_df_to_json, sort_df_by_numeric_col


def test_get_resource_data(mock_get_api_response, mock_data_properties):
    with patch("quote_generator_api.utility.requests.get") as response:
        response.return_value = Mock(status_code=200)
        response.return_value.json.return_value = mock_get_api_response
        actual_data = get_resource_data("https://testabc.com")
    expected_output = mock_data_properties
    assert actual_data == expected_output


def test_convert_to_df(mock_data):
    expected_output = pd.DataFrame(mock_data)
    assert convert_to_df(mock_data).equals(expected_output)


def test_convert_df_to_json(mock_data):
    mock_dataframe = pd.DataFrame(mock_data)
    expected_output = '[{"created":"2025-08-23T20:11:48.569Z","edited":"2025-08-23T20:11:48.569Z","consumables":"2 months","name":"Sand Crawler","cargo_capacity":"50000","passengers":"30","max_atmosphering_speed":"30","crew":"46","length":"36.8 ","model":"Digger Crawler","cost_in_credits":"150000","manufacturer":"Corellia Mining Corporation","vehicle_class":"wheeled","pilots":[],"films":["https:\/\/www.swapi.tech\/api\/films\/1","https:\/\/www.swapi.tech\/api\/films\/5"],"url":"https:\/\/www.swapi.tech\/api\/vehicles\/4"}]'
    assert convert_df_to_json(mock_dataframe) == expected_output


def test_concat_df(mock_data, another_mock_data):
    mock_dataframe = pd.DataFrame(mock_data)
    another_mock_data = pd.DataFrame(another_mock_data)
    expected_output = pd.concat([mock_dataframe, another_mock_data], axis=0, ignore_index=True)
    assert concat_df(mock_dataframe, another_mock_data).equals(expected_output)


def test_filter_df_remove_rows(mock_data):
    mock_dataframe = pd.DataFrame(mock_data)
    assert filter_df(mock_dataframe, column_name='name', value='Sand Crawler', remove_values=True).size == 0


def test_filter_df_maintain_rows(mock_data, another_mock_data):
    mock_dataframe = pd.DataFrame(mock_data)
    another_mock_data = pd.DataFrame(another_mock_data)
    pd.concat([mock_dataframe, another_mock_data], axis=0, ignore_index=True)
    expected_output = mock_dataframe
    assert filter_df(mock_dataframe, column_name='name', value='Sand Crawler').equals(expected_output)


def test_convert_col_to_numeric(mock_data):
    mock_dataframe = pd.DataFrame(mock_data)
    expected_output = pd.DataFrame(
        [{'created': '2025-08-23T20:11:48.569Z', 'edited': '2025-08-23T20:11:48.569Z', 'consumables': '2 months',
          'name': 'Sand Crawler', 'cargo_capacity': '50000', 'passengers': '30', 'max_atmosphering_speed': '30',
          'crew': '46', 'length': '36.8 ', 'model': 'Digger Crawler', 'cost_in_credits': '150000',
          'manufacturer': 'Corellia Mining Corporation', 'vehicle_class': 'wheeled', 'pilots': [],
          'films': ['https://www.swapi.tech/api/films/1', 'https://www.swapi.tech/api/films/5'],
          'url': 'https://www.swapi.tech/api/vehicles/4', 'cargo_capacity_num': 50000}])
    assert convert_col_to_numeric(mock_dataframe, "cargo_capacity", "cargo_capacity_num").equals(expected_output)


def test_sort_df_by_numeric_col(mock_starship_data):
    mock_dataframe = pd.DataFrame(mock_starship_data)
    mock_dataframe_copy = mock_dataframe.copy()
    mock_dataframe_copy = convert_col_to_numeric(mock_dataframe_copy, "MGLT", "MGLT_num")
    expected_output = mock_dataframe_copy.sort_values(by='MGLT_num').reset_index(drop=True).drop("MGLT_num", axis=1)
    assert sort_df_by_numeric_col(convert_col_to_numeric(mock_dataframe, "MGLT", "MGLT_num"), "MGLT_num").equals(expected_output)


def test_sort_df_by_numeric_col_descending_order(mock_starship_data):
    mock_dataframe = pd.DataFrame(mock_starship_data)
    mock_dataframe_copy = mock_dataframe.copy()
    mock_dataframe_copy = convert_col_to_numeric(mock_dataframe_copy, "MGLT", "MGLT_num")
    expected_output = mock_dataframe_copy.sort_values(by='MGLT_num', ascending=False).reset_index(drop=True).drop("MGLT_num", axis=1)
    assert sort_df_by_numeric_col(convert_col_to_numeric(mock_dataframe, "MGLT", "MGLT_num"), "MGLT_num", ascending=False).equals(
        expected_output)


def test_write_multiple_df_to_json(mock_data, another_mock_data):
    mock_df1 = pd.DataFrame(mock_data)
    mock_df2 = pd.DataFrame(another_mock_data)
    write_multiple_df_to_json([mock_df1, mock_df2], ["mock_data", "another_mock_data"], "tests/output/")
    with open("tests/output/sales_vehicle_delivery_quote.json", "r") as read_file:
        output_data = json.load(read_file)

    assert "mock_data" in output_data
    assert "another_mock_data" in output_data
    assert len(output_data["mock_data"]) == 1
    assert len(output_data["another_mock_data"]) == 1