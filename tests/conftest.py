import pytest

@pytest.fixture(scope="module")
def mock_data():
    return [{'created': '2025-08-23T20:11:48.569Z', 'edited': '2025-08-23T20:11:48.569Z', 'consumables': '2 months',
             'name': 'Sand Crawler', 'cargo_capacity': '50000', 'passengers': '30', 'max_atmosphering_speed': '30',
             'crew': '46', 'length': '36.8 ', 'model': 'Digger Crawler', 'cost_in_credits': '150000',
             'manufacturer': 'Corellia Mining Corporation', 'vehicle_class': 'wheeled', 'pilots': [],
             'films': ['https://www.swapi.tech/api/films/1', 'https://www.swapi.tech/api/films/5'],
             'url': 'https://www.swapi.tech/api/vehicles/4'}]

@pytest.fixture(scope="module")
def another_mock_data():
    return [{'created': '2025-08-23T20:11:48.569Z', 'edited': '2025-08-23T20:11:48.569Z', 'consumables': '2 months',
         'name': 'Sand Crawler Test', 'cargo_capacity': '90000', 'passengers': '30', 'max_atmosphering_speed': '30',
         'crew': '46', 'length': '36.8 ', 'model': 'Digger Crawler', 'cost_in_credits': '150000',
         'manufacturer': 'Corellia Mining Corporation', 'vehicle_class': 'wheeled', 'pilots': [],
         'films': ['https://www.swapi.tech/api/films/1', 'https://www.swapi.tech/api/films/5'],
         'url': 'https://www.swapi.tech/api/vehicles/4'}]

@pytest.fixture(scope="module")
def mock_vehicle_list():
    vehicle_list = ["Sand Crawler", "Sand Crawler"]
    return vehicle_list

@pytest.fixture(scope="module")
def mock_get_api_response():
    return {
  "message": "ok",
  "result": [
    {
      "properties": {
        "created": "2025-08-23T20:11:48.569Z",
        "edited": "2025-08-23T20:11:48.569Z",
        "consumables": "2 months",
        "name": "Sand Crawler",
        "cargo_capacity": "50000",
        "passengers": "30",
        "max_atmosphering_speed": "30",
        "crew": "46",
        "length": "36.8 ",
        "model": "Digger Crawler",
        "cost_in_credits": "150000",
        "manufacturer": "Corellia Mining Corporation",
        "vehicle_class": "wheeled",
        "pilots": [],
        "films": [
          "https://www.swapi.tech/api/films/1",
          "https://www.swapi.tech/api/films/5"
        ],
        "url": "https://www.swapi.tech/api/vehicles/4"
      },
      "_id": "5f63a160cf50d100047f97fc",
      "description": "A vehicle",
      "uid": "4",
      "__v": 2
    }
  ],
  "apiVersion": "1.0",
  "timestamp": "2025-08-24T00:25:48.008Z",
  "support": {
    "contact": "admin@swapi.tech",
    "donate": "https://www.paypal.com/donate/?business=2HGAUVTWGR5T2&no_recurring=0&item_name=Support+Swapi+and+keep+the+galaxy%27s+data+free%21+Your+donation+fuels+open-source+innovation+and+helps+us+grow.+Thank+you%21+%F0%9F%9A%80&currency_code=USD",
    "partnerDiscounts": {
      "saberMasters": {
        "link": "https://www.swapi.tech/partner-discount/sabermasters-swapi",
        "details": "Use this link to automatically get $10 off your purchase!"
      },
      "heartMath": {
        "link": "https://www.heartmath.com/ryanc",
        "details": "Looking for some Jedi-like inner peace? Take 10% off your heart-brain coherence tools from the HeartMath Institute!"
      }
    }
  },
  "social": {
    "discord": "https://discord.gg/zWvA6GPeNG",
    "reddit": "https://www.reddit.com/r/SwapiOfficial/",
    "github": "https://github.com/semperry/swapi/blob/main/CONTRIBUTORS.md"
  }
}