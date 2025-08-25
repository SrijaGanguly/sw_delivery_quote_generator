import pandas as pd

from quote_generator_api.starship import pull_starships_urls, pull_starship_data_using_urls, create_starship_df, calculate_num_days_travel, calculate_crew_cost, find_min_crew, calculate_starship_delivery_cost_df
from unittest.mock import patch

from tests.conftest import mock_data


def test_pull_starships_urls(mock_overview_response):
    with patch('quote_generator_api.starship.get_overview_json', return_value=mock_overview_response):
        actual_data = pull_starships_urls()
    expected_data = ['https://www.swapi.tech/api/vehicles/4', 'https://www.swapi.tech/api/vehicles/7',
                     'https://www.swapi.tech/api/vehicles/6', 'https://www.swapi.tech/api/vehicles/8',
                     'https://www.swapi.tech/api/vehicles/14']
    assert actual_data == expected_data


def test_pull_starships_no_urls():
    with patch('quote_generator_api.starship.get_overview_json', return_value=[]):
        actual_data = pull_starships_urls()
    assert actual_data is None


def test_pull_starship_data_using_urls(mock_data):
    with patch('quote_generator_api.starship.pull_starships_urls') as mock_pull_starship_urls_return, \
            patch('quote_generator_api.starship.get_resource_data') as mock_get_resource_data_return:
        mock_pull_starship_urls_return.return_value = ['https://www.swapi.tech/api/vehicles/4',
                                                       'https://www.swapi.tech/api/vehicles/7',
                                                       'https://www.swapi.tech/api/vehicles/6',
                                                       'https://www.swapi.tech/api/vehicles/8',
                                                       'https://www.swapi.tech/api/vehicles/14']
        mock_get_resource_data_return.return_value = mock_data
        actual_data = pull_starship_data_using_urls()
    expected_data = mock_data * 5
    assert actual_data == expected_data


def test_create_starship_df(mock_data, another_mock_data):
    with patch('quote_generator_api.starship.pull_starship_data_using_urls',
               return_value=(mock_data + another_mock_data)):
        actual_data = create_starship_df()
    expected_data = pd.concat([pd.DataFrame(mock_data), pd.DataFrame(another_mock_data)], axis=0, ignore_index=True)
    assert actual_data.equals(expected_data)


def test_calculate_num_days_travel_numeric_inputs():
    starship_mglt = "40"
    distance_mglt_input = "100"
    expected_num_days_travel = (int(distance_mglt_input)/int(starship_mglt))/24
    assert calculate_num_days_travel(starship_mglt, distance_mglt_input) == str(expected_num_days_travel)

def test_calculate_num_days_travel_unknown_inputs():
    starship_mglt = "unknown"
    distance_mglt_input = "100"
    expected_num_days_travel = "NA"
    assert calculate_num_days_travel(starship_mglt, distance_mglt_input) == str(expected_num_days_travel)

def test_calculate_num_days_travel_negative_inputs():
    starship_mglt = "-2"
    distance_mglt_input = "100"
    expected_num_days_travel = "NA"
    assert calculate_num_days_travel(starship_mglt, distance_mglt_input) == str(expected_num_days_travel)


def test_calculate_crew_cost():
    min_crew = "59"
    num_days_travel = "47"
    expected_crew_cost = int(min_crew)*100*float(num_days_travel)
    assert calculate_crew_cost(min_crew, num_days_travel) == str(expected_crew_cost)

def test_calculate_crew_cost_fraction_input():
    min_crew = "59"
    num_days_travel = "0.009"
    expected_crew_cost = int(min_crew)*100*float(num_days_travel)
    assert calculate_crew_cost(min_crew, num_days_travel) == str(expected_crew_cost)


def test_calculate_crew_cost_nonnumeric_inputs():
    min_crew = "59"
    num_days_travel = "NA"
    expected_crew_cost = "NA"
    assert calculate_crew_cost(min_crew, num_days_travel) == expected_crew_cost

def test_calculate_crew_cost_negative_min_crew_inputs():
    min_crew = "-1"
    num_days_travel = "200"
    expected_crew_cost = "NA"
    assert calculate_crew_cost(min_crew, num_days_travel) == expected_crew_cost


def test_find_min_crew_numeric_inputs():
    crew = "10"
    assert find_min_crew(crew) == "10"
    crew = "37,433"
    assert find_min_crew(crew) == "37433"
    crew = "37-500"
    assert find_min_crew(crew) == "37"

def test_find_min_crew_nonnumeric_inputs():
    crew = "unknown"
    assert find_min_crew(crew) == "-1"

def test_calculate_starship_delivery_cost_df(mock_starship_data):
    starship_dataframe = pd.DataFrame(mock_starship_data)
    distance_mglt_input = "109"
    expected_dataframe = pd.DataFrame([{'name': 'Sand Crawler', 'model': 'Digger Crawler', 'min_crew': '46', 'MGLT':'57', 'num_days_to_travel': f'{calculate_num_days_travel("57", distance_mglt_input)}' , 'cost_of_credits_delivery': f'{calculate_crew_cost("46", calculate_num_days_travel("57", distance_mglt_input))}'},
                                       {'name': 'Sand Crawler 2', 'model': 'Digger Crawler', 'min_crew': '87', 'MGLT':'97', 'num_days_to_travel': f'{calculate_num_days_travel("97", distance_mglt_input)}' , 'cost_of_credits_delivery': f'{calculate_crew_cost("87", calculate_num_days_travel("97", distance_mglt_input))}'},
                                       {'name': 'Sand Crawler 3', 'model': 'Digger Crawler', 'min_crew': '-1', 'MGLT':'10', 'num_days_to_travel': f'{calculate_num_days_travel("10", distance_mglt_input)}' , 'cost_of_credits_delivery': f'{calculate_crew_cost("-1", calculate_num_days_travel("10", distance_mglt_input))}'},
                                       {'name': 'Sand Crawler 4', 'model': 'Digger Crawler', 'min_crew': '102100', 'MGLT':'87', 'num_days_to_travel': f'{calculate_num_days_travel("87", distance_mglt_input)}' , 'cost_of_credits_delivery': f'{calculate_crew_cost("102100", calculate_num_days_travel("87", distance_mglt_input))}'},
                                       {'name': 'Sand Crawler 5', 'model': 'Digger Crawler', 'min_crew': '89', 'MGLT':'unknown', 'num_days_to_travel': f'{calculate_num_days_travel("unknown", distance_mglt_input)}' , 'cost_of_credits_delivery': f'{calculate_crew_cost("89", calculate_num_days_travel("unknown", distance_mglt_input))}'}])

    final_dataframe = calculate_starship_delivery_cost_df(starship_dataframe, distance_mglt_input)
    assert final_dataframe.equals(expected_dataframe)