import pandas as pd

from quote_generator_api.starship import pull_starships_urls, pull_starship_data_using_urls, create_starship_df
from unittest.mock import patch

from tests.conftest import mock_data


def test_pull_starships_urls(mock_overview_response):
    with patch('quote_generator_api.starship.get_overview_json', return_value=mock_overview_response):
        actual_data = pull_starships_urls()
    expected_data = ['https://www.swapi.tech/api/vehicles/4', 'https://www.swapi.tech/api/vehicles/7', 'https://www.swapi.tech/api/vehicles/6', 'https://www.swapi.tech/api/vehicles/8','https://www.swapi.tech/api/vehicles/14']
    assert actual_data == expected_data

def test_pull_starships_no_urls():
    with patch('quote_generator_api.starship.get_overview_json', return_value=[]):
        actual_data = pull_starships_urls()
    assert actual_data is None

#todo check
def test_pull_starship_data_using_urls(mock_data):
    with patch('quote_generator_api.starship.pull_starships_urls') as mock_pull_starship_urls_return, \
         patch('quote_generator_api.starship.get_resource_data') as mock_get_resource_data_return:
            mock_pull_starship_urls_return.return_value = ['https://www.swapi.tech/api/vehicles/4', 'https://www.swapi.tech/api/vehicles/7', 'https://www.swapi.tech/api/vehicles/6', 'https://www.swapi.tech/api/vehicles/8','https://www.swapi.tech/api/vehicles/14']
            mock_get_resource_data_return.return_value = mock_data
            actual_data = pull_starship_data_using_urls()
    expected_data = mock_data * 5
    print(actual_data)
    assert actual_data == expected_data


def test_create_starship_df(mock_data, another_mock_data):
    with patch('quote_generator_api.starship.pull_starship_data_using_urls',
               return_value=(mock_data + another_mock_data)):
        actual_data = create_starship_df()
    expected_data = pd.concat([pd.DataFrame(mock_data), pd.DataFrame(another_mock_data)], axis=0, ignore_index=True)
    assert actual_data.equals(expected_data)