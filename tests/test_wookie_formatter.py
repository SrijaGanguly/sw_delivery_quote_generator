from quote_generator_api.wookie_formatter import convert_to_wookie
import json

def test_convert_to_wookie():
    convert_to_wookie("tests/output/sales_vehicle_delivery_quote.json", "tests/output/")

    with open("tests/output/sales_vehicle_delivery_quote_wookie.json", "r") as read_file:
        output_data = json.load(read_file)
    # for "mock_data" block
    assert "scoooaor_waraaora" in output_data
    # for "another_mock_data"
    assert "rawhooaoacworc_scoooaor_waraaora" in output_data
    assert len(output_data["scoooaor_waraaora"]) == 1
    assert len(output_data["rawhooaoacworc_scoooaor_waraaora"]) == 1