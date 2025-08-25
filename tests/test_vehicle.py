from quote_generator_api import vehicle
from quote_generator_api.vehicle import *
from unittest.mock import patch


def test_pull_vehicle_data(mock_data):
    with patch("quote_generator_api.vehicle.get_resource_data", return_value=mock_data):
        actual_data = vehicle.pull_vehicle_data("Sand Crawler")
    expected_output = mock_data
    assert actual_data == expected_output

def test_create_vehicle_df(mock_vehicle_list, mock_data):
    with patch("quote_generator_api.vehicle.pull_vehicle_data", return_value=mock_data):
        actual_data = create_vehicle_df(mock_vehicle_list)
    expected_output = pd.concat([pd.DataFrame(mock_data), pd.DataFrame(mock_data)], axis=0, ignore_index=True)[["name", "length"]]
    assert actual_data.equals(expected_output)
